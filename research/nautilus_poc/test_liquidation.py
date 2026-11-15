"""Liquidation behaviour tests for the isolated NautilusTrader POC."""

from decimal import Decimal

from nautilus_trader.backtest import BacktestEngine
from nautilus_trader.config import BacktestEngineConfig
from nautilus_trader.execution import MakerTakerFeeModel
from nautilus_trader.model import (
    AccountType,
    Currency,
    MarkPriceUpdate,
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


BTC = Currency.from_str("BTC")
VENUE = Venue("BYBIT")
INSTRUMENT = TestInstrumentProvider.btcusd_bybit()


class DirectionalInversePosition(Strategy):
    def __init__(self):
        super().__init__()
        self.side = OrderSide.BUY
        self.submitted = False
        self.fill_events = []

    def on_start(self):
        self.subscribe_quotes(INSTRUMENT.id)

    def on_quote(self, quote):
        if self.submitted:
            return
        self.submitted = True
        self.submit_order(
            self.order_factory.market(
                instrument_id=INSTRUMENT.id,
                order_side=self.side,
                quantity=Quantity.from_int(10_000_000),
            ),
        )

    def on_order_filled(self, event):
        self.fill_events.append(event)


def make_quote(price: int, timestamp: int) -> QuoteTick:
    value = Price.from_str(f"{price}.0")
    return QuoteTick(
        instrument_id=INSTRUMENT.id,
        bid_price=value,
        ask_price=value,
        bid_size=Quantity.from_int(10_000_000),
        ask_size=Quantity.from_int(10_000_000),
        ts_event=timestamp,
        ts_init=timestamp,
    )


def build_engine():
    engine = BacktestEngine(
        BacktestEngineConfig(bypass_logging=True, run_analysis=False),
    )
    engine.add_venue(
        venue=VENUE,
        oms_type=OmsType.NETTING,
        account_type=AccountType.MARGIN,
        base_currency=BTC,
        starting_balances=[Money(1, BTC)],
        fee_model=MakerTakerFeeModel(
            maker_rate=Decimal("-0.00025"),
            taker_rate=Decimal("0.00075"),
        ),
        liquidation_enabled=True,
        liquidation_trigger_ratio=1.0,
        liquidation_cancel_open_orders=True,
    )
    engine.add_instrument(INSTRUMENT)
    return engine


def run_liquidation_case():
    engine = build_engine()
    strategy = DirectionalInversePosition()
    try:
        engine.add_strategy(strategy)
        engine.add_data([
            make_quote(40_000, 1),
            make_quote(20_000, 2),
        ])
        engine.run()
        account = engine.portfolio.account(venue=VENUE)
        return {
            "open_positions": engine.cache.positions_open_count(),
            "closed_positions": engine.cache.positions_closed_count(),
            "balance": account.balance_total(BTC),
            "strategy_fill_count": len(strategy.fill_events),
        }
    finally:
        engine.dispose()


def run_mark_price_precedence_case():
    engine = build_engine()
    strategy = DirectionalInversePosition()
    try:
        engine.add_strategy(strategy)
        engine.add_data([
            # The position opens at 40,000 and the matching-engine book stays there.
            make_quote(40_000, 1),
            # A conflicting 20,000 mark should trigger liquidation before the quote changes.
            MarkPriceUpdate(
                instrument_id=INSTRUMENT.id,
                value=Price.from_str("20000.0"),
                ts_event=2,
                ts_init=2,
            ),
        ])
        engine.run()
        account = engine.portfolio.account(venue=VENUE)
        return {
            "open_positions": engine.cache.positions_open_count(),
            "closed_positions": engine.cache.positions_closed_count(),
            "balance": account.balance_total(BTC),
            "strategy_fill_count": len(strategy.fill_events),
        }
    finally:
        engine.dispose()


def test_maintenance_margin_breach_triggers_synthetic_position_close():
    result = run_liquidation_case()
    assert result["open_positions"] == 0
    assert result["closed_positions"] == 1
    assert result["strategy_fill_count"] == 2
    # The final balance is intentionally not treated as a safe liquidation price:
    # the engine currently models a synthetic close at the observed quote.
    assert result["balance"] == Money.from_str("-249.56250000 BTC")


def test_liquidation_replay_is_deterministic():
    assert run_liquidation_case() == run_liquidation_case()


def test_mark_price_triggers_liquidation_ahead_of_conflicting_quote():
    result = run_mark_price_precedence_case()

    assert result["open_positions"] == 0
    assert result["closed_positions"] == 1
    assert result["strategy_fill_count"] == 2
    # Trigger valuation uses the 20,000 mark; synthetic close execution still uses
    # the matching engine's 40,000 bid. Two taker fees total 0.375 BTC.
    assert result["balance"] == Money.from_str("0.62500000 BTC")


def test_mark_price_precedence_replay_is_deterministic():
    assert run_mark_price_precedence_case() == run_mark_price_precedence_case()



def make_spread_quote(bid: int, ask: int, timestamp: int) -> QuoteTick:
    return QuoteTick(
        instrument_id=INSTRUMENT.id,
        bid_price=Price.from_str(f"{bid}.0"),
        ask_price=Price.from_str(f"{ask}.0"),
        bid_size=Quantity.from_int(10_000_000),
        ask_size=Quantity.from_int(10_000_000),
        ts_event=timestamp,
        ts_init=timestamp,
    )


def run_spread_liquidation_case(position_side: OrderSide):
    engine = build_engine()
    strategy = DirectionalInversePosition()
    strategy.side = position_side
    try:
        engine.add_strategy(strategy)
        engine.add_data([
            make_spread_quote(40_000, 40_000, 1),
            # A 1% spread around 40,000 creates opposite PnL signs depending
            # on which side is used: bid 39,800 is adverse for a long, while
            # ask 40,200 is adverse for a short.
            make_spread_quote(39_800, 40_200, 2),
        ])
        engine.run()
        return {
            "open_positions": engine.cache.positions_open_count(),
            "closed_positions": engine.cache.positions_closed_count(),
            "balance": engine.portfolio.account(venue=VENUE).balance_total(BTC),
            "fill_prices": [event.last_px for event in strategy.fill_events],
        }
    finally:
        engine.dispose()


def test_long_liquidation_valuation_uses_bid_not_favourable_ask():
    result = run_spread_liquidation_case(OrderSide.BUY)

    assert result["open_positions"] == 0
    assert result["closed_positions"] == 1
    assert result["fill_prices"] == [
        Price.from_str("40000.0"),
        Price.from_str("39800.0"),
    ]


def test_short_liquidation_valuation_uses_ask_not_favourable_bid():
    result = run_spread_liquidation_case(OrderSide.SELL)

    assert result["open_positions"] == 0
    assert result["closed_positions"] == 1
    assert result["fill_prices"] == [
        Price.from_str("40000.0"),
        Price.from_str("40200.0"),
    ]


def test_long_and_short_spread_liquidation_replays_are_deterministic():
    assert run_spread_liquidation_case(OrderSide.BUY) == run_spread_liquidation_case(OrderSide.BUY)
    assert run_spread_liquidation_case(OrderSide.SELL) == run_spread_liquidation_case(OrderSide.SELL)
