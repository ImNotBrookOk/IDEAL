from decimal import Decimal

import pytest

from poc import inverse_pnl, linear_pnl, trading_fee, funding_cashflow


def test_linear_contract_pnl_matches_independent_oracle():
    assert linear_pnl(Decimal("60000"), Decimal("61500"), Decimal("0.2"), Decimal("1")) == Decimal("300")


def test_inverse_contract_pnl_is_settled_in_base_currency():
    assert inverse_pnl(Decimal("60000"), Decimal("63000"), Decimal("100"), Decimal("1")) == Decimal("0.00007936507936507936507936508000")


def test_fee_uses_execution_notional():
    assert trading_fee(Decimal("60000"), Decimal("0.2"), Decimal("1"), Decimal("0.0005")) == Decimal("6.00000")


def test_positive_funding_rate_debits_long_and_credits_short():
    notional, rate = Decimal("12000"), Decimal("0.0001")
    assert funding_cashflow(notional, rate, is_long=True) == Decimal("-1.2000")
    assert funding_cashflow(notional, rate, is_long=False) == Decimal("1.2000")


def test_negative_funding_rate_reverses_cashflow():
    assert funding_cashflow(Decimal("12000"), Decimal("-0.0001"), is_long=True) == Decimal("1.2000")
    assert funding_cashflow(Decimal("12000"), Decimal("-0.0001"), is_long=False) == Decimal("-1.2000")


def test_invalid_or_nonpositive_contract_inputs_are_rejected():
    with pytest.raises(ValueError):
        linear_pnl(Decimal("0"), Decimal("10"), Decimal("1"), Decimal("1"))


def test_negative_fee_rate_is_rejected():
    with pytest.raises(ValueError):
        trading_fee(Decimal("10"), Decimal("1"), Decimal("1"), Decimal("-0.01"))



def test_linear_short_pnl_is_the_inverse_of_long_pnl():
    assert linear_pnl(
        Decimal("60000"),
        Decimal("58500"),
        Decimal("0.2"),
        Decimal("1"),
        is_long=False,
    ) == Decimal("300")


def test_inverse_short_pnl_is_the_inverse_of_long_pnl():
    assert inverse_pnl(
        Decimal("60000"),
        Decimal("63000"),
        Decimal("100"),
        Decimal("1"),
        is_long=False,
    ) == Decimal("-0.00007936507936507936507936508000")


def test_contract_pnl_rejects_non_boolean_direction():
    with pytest.raises(ValueError):
        linear_pnl(
            Decimal("60000"),
            Decimal("61000"),
            Decimal("0.1"),
            Decimal("1"),
            is_long="long",
        )
