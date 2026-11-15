from decimal import Decimal

import nautilus_trader
import pytest
from nautilus_trader.backtest import BacktestEngine
from nautilus_trader.config import BacktestEngineConfig
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
    Venue,
)

from poc import (
    inverse_pnl,
    linear_pnl,
    trading_fee,
    funding_cashflow,
)


def test_linear_contract_pnl_matches_independent_oracle():
    assert linear_pnl(
        entry=Decimal("60000"),
        exit=Decimal("61500"),
        quantity=Decimal("0.2"),
        multiplier=Decimal("1"),
    ) == Decimal("300")


def test_inverse_contract_pnl_is_settled_in_base_currency():
    assert inverse_pnl(
        entry=Decimal("60000"),
        exit=Decimal("63000"),
        contracts=Decimal("100"),
        contract_value_quote=Decimal("1"),
    ) == Decimal("0.00007936507936507936507936508000")


def test_fee_uses_execution_notional():
    assert trading_fee(
        price=Decimal("60000"),
        quantity=Decimal("0.2"),
        multiplier=Decimal("1"),
        fee_rate=Decimal("0.0005"),
    ) == Decimal("6.00000")


def test_positive_funding_rate_debits_long_and_credits_short():
    notional = Decimal("12000")
    rate = Decimal("0.0001")
    assert funding_cashflow(notional, rate, is_long=True) == Decimal("-1.2000")
    assert funding_cashflow(notional, rate, is_long=False) == Decimal("1.2000")


def test_invalid_or_nonpositive_contract_inputs_are_rejected():
    with pytest.raises(ValueError):
        linear_pnl(Decimal("0"), Decimal("10"), Decimal("1"), Decimal("1"))


def test_pinned_nautilus_release_and_perpetual_model_construct():
    assert nautilus_trader.__version__ == "2.0.0rc9"
    instrument_id = InstrumentId.from_str("BTCUSDT-PERP.SIM")
    instrument = CryptoPerpetual(
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
        maker_fee=Decimal("0.0002"),
        taker_fee=Decimal("0.0005"),
    )
    assert instrument.id == instrument_id
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
        )
        instrument_id = InstrumentId.from_str("BTCUSDT-PERP.SIM")
        instrument = CryptoPerpetual(
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
            maker_fee=Decimal("0.0002"),
            taker_fee=Decimal("0.0005"),
        )
        engine.add_instrument(instrument)
        assert engine.cache.instrument(instrument_id) is not None
    finally:
        engine.dispose()
