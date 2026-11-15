from decimal import Decimal

import nautilus_trader
from nautilus_trader.backtest import BacktestEngine
from nautilus_trader.config import BacktestEngineConfig
from nautilus_trader.execution import MakerTakerFeeModel
from nautilus_trader.model import (
    AccountType,
    CryptoPerpetual,
    Currency,
    FundingRateUpdate,
    InstrumentId,
    Money,
    OmsType,
    Price,
    Quantity,
    Symbol,
    Venue,
)


def make_instrument():
    instrument_id = InstrumentId.from_str("BTCUSDT-PERP.SIM")
    return CryptoPerpetual(
        instrument_id=instrument_id,
        raw_symbol=instrument_id.symbol,
        base_currency=Currency.from_str("BTC"),
        quote_currency=Currency.from_str("USDT"),
        settlement_currency=Currency.from_str("USDT"),
        is_inverse=False,
        price_precision=2,
        size_precision=3,
        price_increment=Price.from_str("0.01"),
        size_increment=Quantity.from_str("0.001"),
        ts_event=1,
        ts_init=1,
        margin_init=Decimal("0.05"),
        margin_maint=Decimal("0.025"),
    )


def test_pinned_release_and_crypto_perpetual_model_construct():
    assert nautilus_trader.__version__ == "2.0.0rc9"
    instrument = make_instrument()
    assert instrument.id == InstrumentId.from_str("BTCUSDT-PERP.SIM")
    assert instrument.is_inverse is False
    assert instrument.margin_init == Decimal("0.05")


def test_funding_rate_event_model_constructs_with_explicit_boundary():
    event = FundingRateUpdate(
        instrument_id=InstrumentId.from_str("BTCUSDT-PERP.SIM"),
        rate=Decimal("0.0001"),
        interval=480,
        next_funding_ns=8_000_000_000,
        ts_event=1,
        ts_init=1,
    )
    assert event.rate == Decimal("0.0001")
    assert event.next_funding_ns == 8_000_000_000


def test_backtest_margin_venue_and_instrument_register():
    engine = BacktestEngine(BacktestEngineConfig())
    try:
        venue = Venue("SIM")
        engine.add_venue(
            venue=venue,
            oms_type=OmsType.NETTING,
            account_type=AccountType.MARGIN,
            starting_balances=[Money.from_str("10000 USDT")],
            fee_model=MakerTakerFeeModel(
                maker_rate=Decimal("0.0002"),
                taker_rate=Decimal("0.0005"),
            ),
        )
        instrument = make_instrument()
        engine.add_instrument(instrument)
        assert engine.cache.instrument(instrument.id) is not None
    finally:
        engine.dispose()



def test_inverse_crypto_perpetual_uses_base_currency_settlement():
    btc = Currency.from_str("BTC")
    inverse = CryptoPerpetual(
        instrument_id=InstrumentId.from_str("BTCUSD-PERP.SIM"),
        raw_symbol=Symbol("BTCUSD"),
        base_currency=btc,
        quote_currency=Currency.from_str("USD"),
        settlement_currency=btc,
        is_inverse=True,
        price_precision=1,
        size_precision=0,
        price_increment=Price.from_str("0.1"),
        size_increment=Quantity.from_str("1"),
        ts_event=1,
        ts_init=1,
        margin_init=Decimal("0.05"),
        margin_maint=Decimal("0.025"),
    )
    assert inverse.is_inverse is True
    assert inverse.settlement_currency == btc
