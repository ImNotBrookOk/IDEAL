"""Bar-only and trade-only liquidation tests for the isolated NautilusTrader POC.

These fixtures deliberately omit QuoteTick data. They distinguish the source used
to value a maintenance breach from the matching engine's executable close side.
"""

from decimal import Decimal

from nautilus_trader.backtest import BacktestEngine
from nautilus_trader.config import BacktestEngineConfig
from nautilus_trader.execution import MakerTakerFeeModel
from nautilus_trader.model import (
    AccountType,
    AggressorSide,
    Bar,
    BarType,
    BookType,
    Currency,
    Money,
    OmsType,
    OrderSide,
    Price,
    PriceType,
    Quantity,
    TimeInForce,
    TradeId,
    TradeTick,
    Venue,
)
from nautilus_trader.testkit.providers import TestInstrumentProvider
from nautilus_trader.trading import Strategy


BTC = Currency.from_str("BTC")
VENUE = Venue("BYBIT")
INSTRUMENT = TestInstrumentProvider.btcusd_bybit()
BAR_TYPE = BarType.from_str(f"{INSTRUMENT.id}-1-MINUTE-LAST-EXTERNAL")
BASE_NS = 1_700_000_000_000_000_000
CONTRACTS = Quantity.from_int(10_000_000)


class RestingInverseLong(Strategy):
    """Rest a buy limit so a trade or execution bar can open the position."""

    def __init__(self):
        super().__init__()
        self.fill_events = []

    def on_start(self):
        self.submit_order(
            self.order_factory.limit(
                instrument_id=INSTRUMENT.id,
                order_side=OrderSide.BUY,
                quantity=CONTRACTS,
                price=Price.from_str("40000.0"),
                time_in_force=TimeInForce.GTC,
            ),
        )

    def on_order_filled(self, event):
        self.fill_events.append(event)


def make_bar(price: int, offset: int) -> Bar:
    timestamp = BASE_NS + offset
    value = Price.from_str(f"{price}.0")
    return Bar(
        bar_type=BAR_TYPE,
        open=value,
        high=value,
        low=value,
        close=value,
        volume=Quantity.from_int(40_000_000),
        ts_event=timestamp,
        ts_init=timestamp,
    )


def make_trade(price: int, trade_id: str, offset: int) -> TradeTick:
    timestamp = BASE_NS + offset
    return TradeTick(
        instrument_id=INSTRUMENT.id,
        price=Price.from_str(f"{price}.0"),
        size=CONTRACTS,
        aggressor_side=AggressorSide.SELL,
        trade_id=TradeId.from_str(trade_id),
        ts_event=timestamp,
        ts_init=timestamp,
    )


def build_engine(*, bar_execution: bool, trade_execution: bool, book_type=BookType.L1_MBP):
    engine = BacktestEngine(
        BacktestEngineConfig(bypass_logging=True, run_analysis=False),
    )
    engine.add_venue(
        venue=VENUE,
        oms_type=OmsType.NETTING,
        account_type=AccountType.MARGIN,
        base_currency=BTC,
        starting_balances=[Money(1, BTC)],
        book_type=book_type,
        fee_model=MakerTakerFeeModel(
            maker_rate=Decimal("-0.00025"),
            taker_rate=Decimal("0.00075"),
        ),
        bar_execution=bar_execution,
        trade_execution=trade_execution,
        liquidation_enabled=True,
        liquidation_trigger_ratio=1.0,
        liquidation_cancel_open_orders=True,
        use_market_order_acks=True,
    )
    engine.add_instrument(INSTRUMENT)
    return engine


def run_bar_only_liquidation():
    """Bars are the only price data; bar execution supplies the synthetic L1 book."""
    engine = build_engine(bar_execution=True, trade_execution=False)
    strategy = RestingInverseLong()
    try:
        engine.add_strategy(strategy)
        engine.add_data([
            make_bar(40_000, 60_000_000_000),
            make_bar(20_000, 120_000_000_000),
        ])
        engine.run()
        return {
            "open_positions": engine.cache.positions_open_count(),
            "closed_positions": engine.cache.positions_closed_count(),
            "fill_count": len(strategy.fill_events),
            "balance": engine.portfolio.account(venue=VENUE).balance_total(BTC),
        }
    finally:
        engine.dispose()


def run_trade_only_without_quote_book():
    """Trades update last price and fill entry, but L2 book stays empty without depth."""
    engine = build_engine(
        bar_execution=False,
        trade_execution=True,
        book_type=BookType.L2_MBP,
    )
    strategy = RestingInverseLong()
    try:
        engine.add_strategy(strategy)
        engine.add_data([
            make_trade(40_000, "entry-trade", 1_000_000_000),
            make_trade(20_000, "liquidation-trade", 2_000_000_000),
        ])
        engine.run()
        return {
            "open_positions": engine.cache.positions_open_count(),
            "closed_positions": engine.cache.positions_closed_count(),
            "fill_count": len(strategy.fill_events),
            "balance": engine.portfolio.account(venue=VENUE).balance_total(BTC),
            "last_trade": engine.cache.price(INSTRUMENT.id, PriceType.LAST),
        }
    finally:
        engine.dispose()


def test_bar_close_fallback_triggers_liquidation_and_bar_book_executes_close():
    result = run_bar_only_liquidation()

    # No QuoteTick or TradeTick is supplied. The bar close is therefore the
    # available liquidation valuation source. L1 bar execution also supplies
    # the synthetic bid required by the liquidation close path.
    assert result["open_positions"] == 0
    assert result["closed_positions"] == 1
    assert result["fill_count"] == 2


def test_trade_price_fallback_triggers_breach_but_close_is_skipped_without_bid():
    result = run_trade_only_without_quote_book()

    # The trade stream opens the position and moves last price through the
    # maintenance threshold. With an L2 venue and no OrderBookDepth updates,
    # trade_execution can match the entry from LAST while the actual L2 book
    # remains empty. The engine values the breach from LAST but skips closing
    # because best_bid_price() is absent.
    assert result["open_positions"] == 1
    assert result["closed_positions"] == 0
    assert result["fill_count"] == 1
    assert result["last_trade"] == Price.from_str("20000.0")


def test_bar_only_and_trade_only_replays_are_deterministic():
    assert run_bar_only_liquidation() == run_bar_only_liquidation()
    assert run_trade_only_without_quote_book() == run_trade_only_without_quote_book()
