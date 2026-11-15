from decimal import Decimal

from nautilus_trader.backtest import BacktestEngine
from nautilus_trader.config import BacktestEngineConfig
from nautilus_trader.execution import MakerTakerFeeModel
from nautilus_trader.model import (
    AccountType,
    BookType,
    CryptoPerpetual,
    Currency,
    FundingRateUpdate,
    InstrumentId,
    MarkPriceUpdate,
    Money,
    OmsType,
    OrderSide,
    Price,
    Quantity,
    QuoteTick,
    Symbol,
    TimeInForce,
    Venue,
)
from nautilus_trader.testkit.providers import TestInstrumentProvider
from nautilus_trader.trading import Strategy


BTC = Currency.from_str("BTC")
JPY = Currency.from_str("JPY")
USD = Currency.from_str("USD")
USDT = Currency.from_str("USDT")
VENUE = Venue("BINANCE")
BASE_NS = 1_700_000_000_000_000_000

BTCJPY_INSTRUMENT = CryptoPerpetual(
    instrument_id=InstrumentId.from_str("BTCJPY-PERP.BINANCE"),
    raw_symbol=Symbol("BTCJPY"),
    base_currency=BTC,
    quote_currency=JPY,
    settlement_currency=BTC,
    is_inverse=True,
    price_precision=1,
    size_precision=0,
    price_increment=Price.from_str("0.5"),
    size_increment=Quantity.from_str("1"),
    ts_event=0,
    ts_init=0,
    max_notional=Money(10_000_000.0, JPY),
    min_notional=Money(1.0, JPY),
    max_price=Price.from_str("100000000.0"),
    min_price=Price.from_str("0.5"),
    margin_init=Decimal("0.01"),
    margin_maint=Decimal("0.0035"),
)
BTCUSDT_INSTRUMENT = TestInstrumentProvider.btcusdt_perp_binance()


def quote(instrument_id, bid, ask, bid_size, ask_size, offset):
    timestamp = BASE_NS + offset
    return QuoteTick(
        instrument_id=instrument_id,
        bid_price=Price.from_str(bid),
        ask_price=Price.from_str(ask),
        bid_size=Quantity.from_str(bid_size),
        ask_size=Quantity.from_str(ask_size),
        ts_event=timestamp,
        ts_init=timestamp,
    )


class OpenMultiCurrencyPositions(Strategy):
    def __init__(self):
        super().__init__()
        self.submitted = False
        self.fills = []

    def on_start(self):
        self.subscribe_quotes(BTCUSDT_INSTRUMENT.id)

    def on_quote(self, quote_tick):
        if self.submitted:
            return
        self.submitted = True
        orders = (
            (BTCJPY_INSTRUMENT.id, "10000000", "6000000.0"),
            (BTCUSDT_INSTRUMENT.id, "0.100", "60000.0"),
        )
        for instrument_id, quantity, price in orders:
            self.submit_order(
                self.order_factory.limit(
                    instrument_id=instrument_id,
                    order_side=OrderSide.BUY,
                    quantity=Quantity.from_str(quantity),
                    price=Price.from_str(price),
                    time_in_force=TimeInForce.GTC,
                ),
            )

    def on_order_filled(self, event):
        self.fills.append(event)


def run_multi_currency_margin_case(*, include_funding: bool):
    engine = BacktestEngine(BacktestEngineConfig(bypass_logging=True, run_analysis=False))
    engine.add_venue(
        venue=VENUE,
        oms_type=OmsType.HEDGING,
        account_type=AccountType.MARGIN,
        base_currency=None,
        starting_balances=[
            Money.from_str("100000 USD"),
            Money.from_str("2 BTC"),
            Money.from_str("100000 USDT"),
        ],
        book_type=BookType.L1_MBP,
        trade_execution=False,
        liquidity_consumption=True,
        fee_model=MakerTakerFeeModel(maker_rate=Decimal("0"), taker_rate=Decimal("0")),
    )
    engine.add_instrument(BTCJPY_INSTRUMENT)
    engine.add_instrument(BTCUSDT_INSTRUMENT)
    strategy = OpenMultiCurrencyPositions()
    try:
        engine.add_strategy(strategy)
        data = [
            quote(BTCJPY_INSTRUMENT.id, "5999999.5", "6000000.0", "10000000", "10000000", 1_000_000_000),
            quote(BTCUSDT_INSTRUMENT.id, "59999.5", "60000.0", "0.100", "0.100", 1_100_000_000),
            MarkPriceUpdate(
                BTCJPY_INSTRUMENT.id, Price.from_str("6000000.0"),
                BASE_NS + 2_000_000_000, BASE_NS + 2_000_000_000,
            ),
            MarkPriceUpdate(
                BTCUSDT_INSTRUMENT.id, Price.from_str("60000.0"),
                BASE_NS + 2_100_000_000, BASE_NS + 2_100_000_000,
            ),
        ]
        boundary = BASE_NS + 4_000_000_000
        if include_funding:
            data.extend([
                FundingRateUpdate(
                    instrument_id=BTCJPY_INSTRUMENT.id, rate=Decimal("0.0001"),
                    ts_event=BASE_NS + 2_500_000_000, ts_init=BASE_NS + 2_500_000_000,
                    interval=480, next_funding_ns=boundary,
                ),
                FundingRateUpdate(
                    instrument_id=BTCUSDT_INSTRUMENT.id, rate=Decimal("0.0001"),
                    ts_event=BASE_NS + 2_600_000_000, ts_init=BASE_NS + 2_600_000_000,
                    interval=480, next_funding_ns=boundary,
                ),
            ])
        data.append(
            quote(BTCUSDT_INSTRUMENT.id, "59999.5", "60000.0", "0.100", "0.100", 5_000_000_000),
        )
        engine.add_data(data)
        engine.run()
        account = engine.portfolio.account(venue=VENUE)
        return {
            "base_currency": account.base_currency,
            "balances": {
                BTC: account.balance_total(BTC),
                USD: account.balance_total(USD),
                USDT: account.balance_total(USDT),
            },
            "fill_count": len(strategy.fills),
            "open_positions": engine.cache.positions_open_count(),
        }
    finally:
        engine.dispose()


def test_multi_currency_margin_account_settles_funding_in_native_currencies():
    baseline = run_multi_currency_margin_case(include_funding=False)
    funded = run_multi_currency_margin_case(include_funding=True)

    assert baseline["base_currency"] is None
    assert funded["base_currency"] is None
    assert baseline["fill_count"] == funded["fill_count"] == 2
    assert baseline["open_positions"] == funded["open_positions"] == 2

    # The inverse BTCJPY position settles in BTC; the linear BTCUSDT position
    # settles in USDT. With no account base currency, funding remains native.
    assert all(balance is not None for balance in baseline["balances"].values())
    assert baseline["balances"][BTC] - funded["balances"][BTC] == Money.from_str("0.00016667 BTC")
    assert baseline["balances"][USDT] - funded["balances"][USDT] == Money.from_str("0.60000000 USDT")
    assert funded["balances"][USD] == baseline["balances"][USD] == Money.from_str("100000 USD")
