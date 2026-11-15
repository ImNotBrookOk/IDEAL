from decimal import Decimal

import pytest

from nautilus_trader.backtest import BacktestEngine
from nautilus_trader.config import BacktestEngineConfig
from nautilus_trader.execution import MakerTakerFeeModel
from nautilus_trader.model import (
    AccountType,
    BookAction,
    BookOrder,
    BookType,
    Currency,
    FundingRateUpdate,
    Money,
    OmsType,
    OrderBookDelta,
    OrderBookDeltas,
    OrderSide,
    Price,
    Quantity,
    QuoteTick,
    RecordFlag,
    Venue,
)
from nautilus_trader.testkit.providers import TestInstrumentProvider
from nautilus_trader.trading import Strategy


INSTRUMENT = TestInstrumentProvider.btcusdt_perp_binance()
VENUE = Venue("BINANCE")
USDT = Currency.from_str("USDT")
BASE_NS = 1_700_000_000_000_000_000


class OpenLong(Strategy):
    def __init__(self):
        super().__init__()
        self.submitted = False
        self.fills = []

    def on_start(self):
        self.subscribe_quotes(INSTRUMENT.id)

    def on_quote(self, quote):
        if self.submitted:
            return
        self.submitted = True
        self.submit_order(
            self.order_factory.market(
                instrument_id=INSTRUMENT.id,
                order_side=OrderSide.BUY,
                quantity=Quantity.from_str("0.100"),
            ),
        )

    def on_order_filled(self, event):
        self.fills.append(event)


def l2_book(timestamp: int):
    deltas = [
        OrderBookDelta(
            instrument_id=INSTRUMENT.id,
            action=BookAction.ADD,
            order=BookOrder(
                OrderSide.BUY,
                Price.from_str("39999.0"),
                Quantity.from_str("1.000"),
                1,
            ),
            flags=0,
            sequence=1,
            ts_event=timestamp,
            ts_init=timestamp,
        ),
        OrderBookDelta(
            instrument_id=INSTRUMENT.id,
            action=BookAction.ADD,
            order=BookOrder(
                OrderSide.SELL,
                Price.from_str("40001.0"),
                Quantity.from_str("1.000"),
                2,
            ),
            flags=RecordFlag.F_LAST.value,
            sequence=2,
            ts_event=timestamp,
            ts_init=timestamp,
        ),
    ]
    return OrderBookDeltas(INSTRUMENT.id, deltas)


def clear_l2_book(timestamp: int):
    deltas = [
        OrderBookDelta(
            instrument_id=INSTRUMENT.id,
            action=BookAction.CLEAR,
            order=BookOrder(
                OrderSide.BUY,
                Price.from_str("39999.0"),
                Quantity.from_str("0.000"),
                0,
            ),
            flags=0,
            sequence=3,
            ts_event=timestamp,
            ts_init=timestamp,
        ),
        OrderBookDelta(
            instrument_id=INSTRUMENT.id,
            action=BookAction.CLEAR,
            order=BookOrder(
                OrderSide.SELL,
                Price.from_str("40001.0"),
                Quantity.from_str("0.000"),
                0,
            ),
            flags=RecordFlag.F_LAST.value,
            sequence=4,
            ts_event=timestamp,
            ts_init=timestamp,
        ),
    ]
    return OrderBookDeltas(INSTRUMENT.id, deltas)


def quote(timestamp: int):
    return QuoteTick(
        instrument_id=INSTRUMENT.id,
        bid_price=Price.from_str("39999.0"),
        ask_price=Price.from_str("40001.0"),
        bid_size=Quantity.from_str("1.000"),
        ask_size=Quantity.from_str("1.000"),
        ts_event=timestamp,
        ts_init=timestamp,
    )


def funding_update(timestamp: int, boundary: int):
    return FundingRateUpdate(
        instrument_id=INSTRUMENT.id,
        rate=Decimal("0.0001"),
        ts_event=timestamp,
        ts_init=timestamp,
        interval=480,
        next_funding_ns=boundary,
    )


def run_without_settlement_price():
    engine = BacktestEngine(
        BacktestEngineConfig(bypass_logging=True, run_analysis=False),
    )
    engine.add_venue(
        venue=VENUE,
        oms_type=OmsType.NETTING,
        account_type=AccountType.MARGIN,
        starting_balances=[Money.from_str("10000 USDT")],
        book_type=BookType.L2_MBP,
        trade_execution=False,
        liquidity_consumption=True,
        fee_model=MakerTakerFeeModel(
            maker_rate=Decimal("0"),
            taker_rate=Decimal("0"),
        ),
    )
    engine.add_instrument(INSTRUMENT)
    strategy = OpenLong()
    try:
        engine.add_strategy(strategy)
        engine.add_data([
            l2_book(BASE_NS + 1_000_000_000),
            quote(BASE_NS + 2_000_000_000),
            funding_update(BASE_NS + 3_000_000_000, BASE_NS + 5_000_000_000),
            clear_l2_book(BASE_NS + 4_000_000_000),
            # This later quote should not silently recover the failed settlement
            # within the same backtest run.
            quote(BASE_NS + 6_000_000_000),
        ])
        with pytest.raises(RuntimeError, match="Funding settlement failed"):
            engine.run()
        return {
            "fills": list(strategy.fills),
            "open_positions": engine.cache.positions_open_count(),
        }
    finally:
        engine.dispose()


def test_missing_mark_and_top_of_book_causes_fatal_funding_failure():
    result = run_without_settlement_price()

    assert len(result["fills"]) == 1
    assert result["open_positions"] == 1
