from decimal import Decimal

from nautilus_trader.backtest import BacktestEngine
from nautilus_trader.config import BacktestEngineConfig
from nautilus_trader.execution import MakerTakerFeeModel
from nautilus_trader.model import (
    AccountType,
    BookType,
    CryptoPerpetual,
    Currency,
    InstrumentId,
    Money,
    OmsType,
    OrderSide,
    Price,
    Quantity,
    QuoteTick,
    StandardMarginModel,
    Symbol,
    TimeInForce,
    Venue,
)
from nautilus_trader.trading import Strategy


BASE_NS = 1_700_000_000_000_000_000
INSTRUMENT_ID = InstrumentId.from_str("BTCUSDT-PERP.SIM")
USDT = Currency.from_str("USDT")


def make_instrument():
    return CryptoPerpetual(
        instrument_id=INSTRUMENT_ID,
        raw_symbol=Symbol("BTCUSDT"),
        base_currency=Currency.from_str("BTC"),
        quote_currency=USDT,
        settlement_currency=USDT,
        is_inverse=False,
        price_precision=2,
        size_precision=3,
        price_increment=Price.from_str("0.01"),
        size_increment=Quantity.from_str("0.001"),
        ts_event=BASE_NS,
        ts_init=BASE_NS,
        margin_init=Decimal("0.05"),
        margin_maint=Decimal("0.025"),
    )


def make_quote(mid: Decimal, offset: int) -> QuoteTick:
    bid = mid - Decimal("0.50")
    ask = mid + Decimal("0.50")
    timestamp = BASE_NS + offset
    return QuoteTick(
        instrument_id=INSTRUMENT_ID,
        bid_price=Price.from_str(str(bid)),
        ask_price=Price.from_str(str(ask)),
        bid_size=Quantity.from_str("1.000"),
        ask_size=Quantity.from_str("1.000"),
        ts_event=timestamp,
        ts_init=timestamp,
    )


class SubmitOneMarketBuy(Strategy):
    def __init__(self):
        super().__init__()
        self.events = []
        self.fills = []

    def on_start(self):
        self.subscribe_quotes(INSTRUMENT_ID)

    def on_quote(self, quote):
        if self.events:
            return
        order = self.order_factory.market(
            instrument_id=INSTRUMENT_ID,
            order_side=OrderSide.BUY,
            quantity=Quantity.from_str("0.100"),
        )
        self.submit_order(order)

    def on_order_submitted(self, event):
        self.events.append("submitted")

    def on_order_accepted(self, event):
        self.events.append("accepted")

    def on_order_filled(self, event):
        self.events.append("filled")
        self.fills.append(event)


def build_engine():
    engine = BacktestEngine(
        BacktestEngineConfig(bypass_logging=True, run_analysis=False),
    )
    engine.add_venue(
        venue=Venue("SIM"),
        oms_type=OmsType.NETTING,
        account_type=AccountType.MARGIN,
        starting_balances=[Money.from_str("10000 USDT")],
        book_type=BookType.L1_MBP,
        fee_model=MakerTakerFeeModel(
            maker_rate=Decimal("0.0002"),
            taker_rate=Decimal("0.0005"),
        ),
        liquidity_consumption=True,
        margin_model=StandardMarginModel(),
        use_market_order_acks=True,
    )
    engine.add_instrument(make_instrument())
    return engine


def run_once():
    engine = build_engine()
    strategy = SubmitOneMarketBuy()
    try:
        engine.add_strategy(strategy)
        engine.add_data([
            make_quote(Decimal("60000"), 1_000_000_000),
            make_quote(Decimal("60001"), 2_000_000_000),
            make_quote(Decimal("60002"), 3_000_000_000),
        ])
        engine.run()
        return {
            "events": list(strategy.events),
            "fill_count": len(strategy.fills),
            "open_positions": engine.cache.positions_open_count(),
            "closed_positions": engine.cache.positions_closed_count(),
            "maintenance_margin": engine.portfolio.account(venue=Venue("SIM")).total_maintenance_margin(USDT),
        }
    finally:
        engine.dispose()


def test_market_order_completes_submit_accept_fill_and_opens_position():
    result = run_once()
    assert result["events"] == ["submitted", "accepted", "filled"]
    assert result["fill_count"] == 1
    assert result["open_positions"] == 1
    assert result["closed_positions"] == 0
    assert result["maintenance_margin"] == Money.from_str("150.00125000 USDT")


def test_identical_synthetic_replay_has_identical_lifecycle_result():
    assert run_once() == run_once()



class RestingLimitBuy(Strategy):
    def __init__(self):
        super().__init__()
        self.accepted = 0

    def on_start(self):
        self.subscribe_quotes(INSTRUMENT_ID)

    def on_quote(self, quote):
        if self.accepted:
            return
        order = self.order_factory.limit(
            instrument_id=INSTRUMENT_ID,
            order_side=OrderSide.BUY,
            quantity=Quantity.from_str("0.100"),
            price=Price.from_str("59999.00"),
            time_in_force=TimeInForce.GTC,
        )
        self.submit_order(order)

    def on_order_accepted(self, event):
        self.accepted += 1


def run_pending_limit_order():
    engine = build_engine()
    strategy = RestingLimitBuy()
    try:
        engine.add_strategy(strategy)
        engine.add_data([make_quote(Decimal("60000"), 1_000_000_000)])
        engine.run()
        account = engine.portfolio.account(venue=Venue("SIM"))
        return {
            "accepted": strategy.accepted,
            "open_orders": engine.cache.orders_open_count(),
            "initial_margin": account.total_initial_margin(USDT),
            "maintenance_margin": account.total_maintenance_margin(USDT),
        }
    finally:
        engine.dispose()


def test_resting_limit_order_reserves_initial_margin():
    result = run_pending_limit_order()
    assert result["accepted"] == 1
    assert result["open_orders"] == 1
    assert result["initial_margin"] == Money.from_str("299.99500000 USDT")
    assert result["maintenance_margin"] == Money.from_str("0.00000000 USDT")
