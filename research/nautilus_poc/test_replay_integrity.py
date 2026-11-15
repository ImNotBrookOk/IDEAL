from decimal import Decimal
from copy import deepcopy

import pytest

from nautilus_trader.backtest import BacktestEngine
from nautilus_trader.config import BacktestEngineConfig
from nautilus_trader.execution import MakerTakerFeeModel
from nautilus_trader.model import (
    AccountType,
    BookType,
    Currency,
    Money,
    OmsType,
    OrderSide,
    Price,
    Quantity,
    QuoteTick,
    Venue,
)
from nautilus_trader.testkit.providers import TestInstrumentProvider
from nautilus_trader.trading import Strategy

from replay_audit import SCHEMA, canonical_bytes, canonical_digest


INSTRUMENT = TestInstrumentProvider.btcusdt_perp_binance()
VENUE = Venue("BINANCE")
USDT = Currency.from_str("USDT")


class RoundTripStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.quote_count = 0
        self.exit_submitted = False
        self.fills = []

    def on_start(self):
        self.subscribe_quotes(INSTRUMENT.id)

    def on_quote(self, quote):
        self.quote_count += 1
        if self.quote_count == 1:
            self.submit_order(
                self.order_factory.market(
                    instrument_id=INSTRUMENT.id,
                    order_side=OrderSide.BUY,
                    quantity=Quantity.from_str("0.100"),
                ),
            )
        elif self.quote_count == 2 and not self.exit_submitted:
            self.exit_submitted = True
            self.submit_order(
                self.order_factory.market(
                    instrument_id=INSTRUMENT.id,
                    order_side=OrderSide.SELL,
                    quantity=Quantity.from_str("0.100"),
                ),
            )

    def on_order_filled(self, event):
        self.fills.append({
            "client_order_id": str(event.client_order_id),
            "instrument_id": str(event.instrument_id),
            "last_qty": str(event.last_qty),
            "last_px": str(event.last_px),
            "ts_event": int(event.ts_event),
        })

    def on_reset(self):
        self.quote_count = 0
        self.exit_submitted = False
        self.fills = []


def make_quote(timestamp: int, bid: str, ask: str) -> QuoteTick:
    return QuoteTick(
        instrument_id=INSTRUMENT.id,
        bid_price=Price.from_str(bid),
        ask_price=Price.from_str(ask),
        bid_size=Quantity.from_str("10.000"),
        ask_size=Quantity.from_str("10.000"),
        ts_event=timestamp,
        ts_init=timestamp,
    )


def build_replay_engine():
    engine = BacktestEngine(
        BacktestEngineConfig(bypass_logging=True, run_analysis=False),
    )
    engine.add_venue(
        venue=VENUE,
        oms_type=OmsType.NETTING,
        account_type=AccountType.MARGIN,
        base_currency=USDT,
        starting_balances=[Money.from_str("10000 USDT")],
        book_type=BookType.L1_MBP,
        trade_execution=True,
        use_market_order_acks=True,
        fee_model=MakerTakerFeeModel(
            maker_rate=Decimal("0.0002"),
            taker_rate=Decimal("0.0005"),
        ),
    )
    engine.add_instrument(INSTRUMENT)
    strategy = RoundTripStrategy()
    engine.add_strategy(strategy)
    engine.add_data([
        make_quote(1_000_000_000, "40000.0", "40001.0"),
        make_quote(2_000_000_000, "40010.0", "40011.0"),
    ])
    return engine, strategy


def capture_replay_snapshot(engine, strategy):
    result = engine.get_result()
    account = engine.portfolio.account(venue=VENUE)
    identity_map = {}
    canonical_fills = []
    for fill in strategy.fills:
        raw_id = fill["client_order_id"]
        if raw_id not in identity_map:
            identity_map[raw_id] = "order-" + str(len(identity_map) + 1).zfill(4)
        canonical_fills.append({**fill, "client_order_id": identity_map[raw_id]})
    return {
        "schema": SCHEMA,
        "run": {
            "iterations": int(result.iterations),
            "total_events": int(result.total_events),
            "total_orders": int(result.total_orders),
            "total_positions": int(result.total_positions),
        },
        "summary": dict(result.summary),
        "fills": canonical_fills,
        "account": {
            "currency": "USDT",
            "balance_total": str(account.balance_total(USDT)),
        },
        "positions": {
            "open": int(engine.cache.positions_open_count()),
            "closed": int(engine.cache.positions_closed_count()),
        },
    }


def run_fresh_replay():
    engine, strategy = build_replay_engine()
    try:
        engine.run()
        snapshot = capture_replay_snapshot(engine, strategy)
        return snapshot
    finally:
        engine.dispose()


def test_canonical_replay_digest_is_stable_across_fresh_engines():
    first = run_fresh_replay()
    second = run_fresh_replay()

    assert first == second
    assert canonical_digest(first) == canonical_digest(second)
    assert len(first["fills"]) == 2
    assert first["positions"] == {"open": 0, "closed": 1}


def test_engine_reset_replay_produces_identical_canonical_digest():
    engine, strategy = build_replay_engine()
    try:
        engine.run()
        first = capture_replay_snapshot(engine, strategy)
        first_digest = canonical_digest(first)
        first_raw_ids = [fill["client_order_id"] for fill in strategy.fills]

        # v2.0.0rc9 reset retains loaded data and resets iterator cursors.
        # Its order ID generator continues, so raw IDs differ after reset.
        engine.reset()
        engine.run()
        second = capture_replay_snapshot(engine, strategy)
        second_raw_ids = [fill["client_order_id"] for fill in strategy.fills]

        assert first_raw_ids != second_raw_ids
        assert first == second
        assert first_digest == canonical_digest(second)
    finally:
        engine.dispose()


def test_canonical_digest_changes_when_fill_or_account_state_changes():
    snapshot = run_fresh_replay()
    changed_fill = deepcopy(snapshot)
    changed_fill["fills"][0]["last_px"] = "40002.0"
    changed_account = deepcopy(snapshot)
    changed_account["account"]["balance_total"] = "9999.00 USDT"

    digest = canonical_digest(snapshot)
    assert canonical_digest(changed_fill) != digest
    assert canonical_digest(changed_account) != digest


def test_canonical_json_is_mapping_order_independent_and_rejects_floats():
    left = {"schema": SCHEMA, "run": {"orders": 2, "events": 4}, "value": "1.25"}
    right = {"value": "1.25", "run": {"events": 4, "orders": 2}, "schema": SCHEMA}

    assert canonical_bytes(left) == canonical_bytes(right)

    with pytest.raises(TypeError, match="floating-point values are not canonical"):
        canonical_bytes({"schema": SCHEMA, "value": 1.25})
