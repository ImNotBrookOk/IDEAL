from decimal import Decimal

from nautilus_trader.backtest import BacktestEngine
from nautilus_trader.config import BacktestEngineConfig
from nautilus_trader.execution import MakerTakerFeeModel
from nautilus_trader.model import (
    AccountType,
    Bar,
    BarType,
    BookType,
    ContingencyType,
    Currency,
    Money,
    OmsType,
    OrderSide,
    OrderType,
    Price,
    Quantity,
    QuoteTick,
    TimeInForce,
    Venue,
)
from nautilus_trader.testkit.providers import TestInstrumentProvider
from nautilus_trader.trading import Strategy


INSTRUMENT = TestInstrumentProvider.btcusdt_perp_binance()
VENUE = Venue("BINANCE")
USDT = Currency.from_str("USDT")
BAR_TYPE = BarType.from_str(
    "BTCUSDT-PERP.BINANCE-1-MINUTE-LAST-EXTERNAL",
)


class AmbiguousBracketStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.submitted = False
        self.fills = []
        self.triggered = []
        self.canceled = []
        self.tp_order_id = None
        self.sl_order_id = None

    def on_start(self):
        self.subscribe_quotes(INSTRUMENT.id)

    def on_quote(self, quote):
        if self.submitted:
            return
        self.submitted = True
        bracket = self.order_factory.bracket(
            instrument_id=INSTRUMENT.id,
            order_side=OrderSide.BUY,
            quantity=Quantity.from_str("0.100"),
            contingency_type=ContingencyType.OCO,
            entry_order_type=OrderType.MARKET,
            tp_price=Price.from_str("40010.0"),
            sl_trigger_price=Price.from_str("39990.0"),
            time_in_force=TimeInForce.GTC,
        )
        self.sl_order_id = bracket[1].client_order_id
        self.tp_order_id = bracket[2].client_order_id
        self.submit_order_list(bracket)

    def on_order_filled(self, event):
        self.fills.append(event)

    def on_order_triggered(self, event):
        self.triggered.append(event)

    def on_order_canceled(self, event):
        self.canceled.append(event)


def make_quote(timestamp: int) -> QuoteTick:
    return QuoteTick(
        instrument_id=INSTRUMENT.id,
        bid_price=Price.from_str("39999.5"),
        ask_price=Price.from_str("40000.5"),
        bid_size=Quantity.from_str("10.000"),
        ask_size=Quantity.from_str("10.000"),
        ts_event=timestamp,
        ts_init=timestamp,
    )


def make_ambiguous_bar(timestamp: int) -> Bar:
    # Both exit thresholds are inside this bar's range. OHLC cannot reveal
    # whether the high or low occurred first.
    return Bar(
        bar_type=BAR_TYPE,
        open=Price.from_str("40000.0"),
        high=Price.from_str("40012.0"),
        low=Price.from_str("39988.0"),
        close=Price.from_str("40001.0"),
        volume=Quantity.from_str("1.000"),
        ts_event=timestamp,
        ts_init=timestamp,
    )


def run_ambiguous_bar_case(adaptive_ordering: bool):
    engine = BacktestEngine(
        BacktestEngineConfig(bypass_logging=True, run_analysis=False),
    )
    engine.add_venue(
        venue=VENUE,
        oms_type=OmsType.NETTING,
        account_type=AccountType.MARGIN,
        base_currency=USDT,
        starting_balances=[Money(100_000, USDT)],
        book_type=BookType.L1_MBP,
        bar_execution=True,
        bar_adaptive_high_low_ordering=adaptive_ordering,
        trade_execution=True,
        liquidity_consumption=True,
        fee_model=MakerTakerFeeModel(
            maker_rate=Decimal("0"),
            taker_rate=Decimal("0"),
        ),
    )
    engine.add_instrument(INSTRUMENT)
    strategy = AmbiguousBracketStrategy()
    try:
        engine.add_strategy(strategy)
        engine.add_data([
            make_quote(1_000_000_000),
            make_ambiguous_bar(61_000_000_000),
        ])
        engine.run()
        return {
            "fills": list(strategy.fills),
            "triggered": list(strategy.triggered),
            "canceled": list(strategy.canceled),
            "open_positions": engine.cache.positions_open_count(),
            "closed_positions": engine.cache.positions_closed_count(),
            "open_orders": engine.cache.orders_open_count(),
            "tp_order_id": strategy.tp_order_id,
            "sl_order_id": strategy.sl_order_id,
        }
    finally:
        engine.dispose()


def test_ambiguous_bar_default_high_first_path_selects_take_profit():
    result = run_ambiguous_bar_case(adaptive_ordering=False)

    # Default synthetic path is O-H-L-C: TP is reached before SL.
    assert len(result["fills"]) == 2
    exit_fill = next(fill for fill in result["fills"] if fill.client_order_id == result["tp_order_id"])
    assert exit_fill.last_px == Price.from_str("40010.0")
    assert result["closed_positions"] == 1
    assert result["open_positions"] == 0


def test_ambiguous_bar_adaptive_low_first_path_selects_stop_loss():
    result = run_ambiguous_bar_case(adaptive_ordering=True)

    # Low is closer to open than high, so adaptive ordering is O-L-H-C.
    # The stop is reached first and the OCO sibling TP is canceled.
    assert len(result["fills"]) == 2
    exit_fill = next(fill for fill in result["fills"] if fill.client_order_id == result["sl_order_id"])
    assert exit_fill.last_px == Price.from_str("39990.0")
    assert result["closed_positions"] == 1
    assert result["open_positions"] == 0
