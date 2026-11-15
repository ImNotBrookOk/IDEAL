"""Research-only tests for reporting-currency conversion in multi-currency accounts."""

from decimal import Decimal

import pytest

from nautilus_trader.backtest import BacktestEngine
from nautilus_trader.config import BacktestEngineConfig
from nautilus_trader.execution import MakerTakerFeeModel
from nautilus_trader.model import (
    AccountType,
    BookType,
    Currency,
    CurrencyPair,
    InstrumentId,
    Money,
    OmsType,
    OrderSide,
    Price,
    Quantity,
    QuoteTick,
    Symbol,
    Venue,
)
from nautilus_trader.testkit.providers import TestInstrumentProvider
from nautilus_trader.trading import Strategy


BTC = Currency.from_str("BTC")
USD = Currency.from_str("USD")
USDT = Currency.from_str("USDT")
VENUE = Venue("BINANCE")
BASE_NS = 1_700_000_000_000_000_000

BTCUSDT_INSTRUMENT = TestInstrumentProvider.btcusdt_perp_binance()
USDTUSD_INSTRUMENT = CurrencyPair(
    instrument_id=InstrumentId.from_str("USDT/USD.BINANCE"),
    raw_symbol=Symbol("USDT/USD"),
    base_currency=USDT,
    quote_currency=USD,
    price_precision=5,
    size_precision=0,
    price_increment=Price.from_str("0.00001"),
    size_increment=Quantity.from_str("1"),
    ts_event=0,
    ts_init=0,
    lot_size=Quantity.from_str("1000"),
    max_quantity=Quantity.from_str("10000000"),
    min_quantity=Quantity.from_str("1000"),
    max_notional=Money(50_000_000.0, USD),
    min_notional=Money(1_000.0, USD),
    margin_init=Decimal("0.03"),
    margin_maint=Decimal("0.03"),
)


def make_quote(instrument_id, bid: str, ask: str, offset: int, size: str) -> QuoteTick:
    timestamp = BASE_NS + offset
    return QuoteTick(
        instrument_id=instrument_id,
        bid_price=Price.from_str(bid),
        ask_price=Price.from_str(ask),
        bid_size=Quantity.from_str(size),
        ask_size=Quantity.from_str(size),
        ts_event=timestamp,
        ts_init=timestamp,
    )


class OpenBtcUsdtLong(Strategy):
    def __init__(self):
        super().__init__()
        self.submitted = False
        self.fills = []

    def on_start(self):
        self.subscribe_quotes(BTCUSDT_INSTRUMENT.id)

    def on_quote(self, quote):
        if self.submitted:
            return
        self.submitted = True
        self.submit_order(
            self.order_factory.market(
                instrument_id=BTCUSDT_INSTRUMENT.id,
                order_side=OrderSide.BUY,
                quantity=Quantity.from_str("0.100"),
            ),
        )

    def on_order_filled(self, event):
        self.fills.append(event)


def build_reporting_currency_case(*, include_conversion: bool = True):
    engine = BacktestEngine(
        BacktestEngineConfig(bypass_logging=True, run_analysis=False),
    )
    engine.add_venue(
        venue=VENUE,
        oms_type=OmsType.NETTING,
        account_type=AccountType.MARGIN,
        base_currency=None,
        starting_balances=[
            Money.from_str("2 BTC"),
            Money.from_str("1000 USDT"),
        ],
        book_type=BookType.L1_MBP,
        trade_execution=False,
        liquidity_consumption=True,
        fee_model=MakerTakerFeeModel(
            maker_rate=Decimal("0"),
            taker_rate=Decimal("0"),
        ),
    )
    engine.add_instrument(BTCUSDT_INSTRUMENT)
    data = []
    if include_conversion:
        engine.add_instrument(USDTUSD_INSTRUMENT)
        data.append(
            make_quote(USDTUSD_INSTRUMENT.id, "0.99950", "1.00050", 1_000_000_000, "1000000"),
        )
    data.extend([
        make_quote(BTCUSDT_INSTRUMENT.id, "59999.5", "60000.0", 2_000_000_000, "0.100"),
    ])
    if include_conversion:
        # The latest conversion quote changes the USDT/USD mid from 1.0 to 0.9.
        data.append(
            make_quote(USDTUSD_INSTRUMENT.id, "0.89950", "0.90050", 3_000_000_000, "1000000"),
        )
    data.append(
        make_quote(BTCUSDT_INSTRUMENT.id, "61000.0", "61000.5", 4_000_000_000, "0.100"),
    )
    strategy = OpenBtcUsdtLong()
    try:
        engine.add_strategy(strategy)
        engine.add_data(data)
        engine.run()
        return engine
    except Exception:
        engine.dispose()
        raise


def test_multi_currency_equity_stays_native_but_pnl_can_convert_at_latest_fx_mid():
    engine = build_reporting_currency_case(include_conversion=True)
    try:
        assert engine.cache.positions_open_count() == 1
        equity = engine.portfolio.equity(venue=VENUE)

        # Equity remains a native-currency map for base_currency=None accounts.
        assert equity[BTC] == Money.from_str("2 BTC")
        assert equity[USDT] == Money.from_str("1100.00000000 USDT")
        assert USD not in equity

        # The open 0.1 BTCUSDT long has +100 USDT unrealized PnL.
        # The latest USDT/USD quote has a 0.90000 mid, so the explicit USD
        # query returns 90 USD (not the 100 USD implied by the older 1.00000 mid).
        assert engine.portfolio.unrealized_pnls(
            venue=VENUE,
            target_currency=USD,
        ) == {USD: Money.from_str("90.00 USD")}
    finally:
        engine.dispose()


def test_explicit_reporting_currency_query_fails_closed_after_cached_fx_is_purged():
    engine = build_reporting_currency_case(include_conversion=True)
    try:
        portfolio = engine.portfolio
        assert portfolio.unrealized_pnls(
            venue=VENUE,
            target_currency=USD,
        ) == {USD: Money.from_str("90.00 USD")}

        # The Portfolio has seen and cached a valid rate. Removing the conversion
        # instrument removes the current rate; explicit target_currency queries
        # must not silently fall back to the cached stale rate.
        engine.cache.purge_instrument(USDTUSD_INSTRUMENT.id)
        with pytest.raises(RuntimeError, match="failed to calculate unrealized PnLs"):
            portfolio.unrealized_pnls(venue=VENUE, target_currency=USD)
    finally:
        engine.dispose()


def test_reporting_currency_query_fails_closed_when_no_fx_rate_has_ever_existed():
    engine = build_reporting_currency_case(include_conversion=False)
    try:
        assert engine.cache.positions_open_count() == 1
        with pytest.raises(RuntimeError, match="failed to calculate unrealized PnLs"):
            engine.portfolio.unrealized_pnls(venue=VENUE, target_currency=USD)
    finally:
        engine.dispose()
