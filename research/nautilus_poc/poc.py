"""Independent decimal arithmetic oracles for the NautilusTrader POC.

These functions are deliberately not IDEAL runtime code. They provide expected
values against which engine behaviour can be compared.
"""
from decimal import Decimal


def _positive(name: str, value: Decimal) -> None:
    if not isinstance(value, Decimal) or not value.is_finite() or value <= 0:
        raise ValueError(f"{name} must be a finite positive Decimal")


def linear_pnl(
    entry: Decimal,
    exit: Decimal,
    quantity: Decimal,
    multiplier: Decimal,
    *,
    is_long: bool = True,
) -> Decimal:
    """Linear contract PnL in quote settlement currency."""
    _positive("entry", entry)
    _positive("exit", exit)
    _positive("quantity", quantity)
    _positive("multiplier", multiplier)
    if not isinstance(is_long, bool):
        raise ValueError("is_long must be bool")
    direction = Decimal(1) if is_long else Decimal(-1)
    return (exit - entry) * quantity * multiplier * direction


def inverse_pnl(
    entry: Decimal,
    exit: Decimal,
    contracts: Decimal,
    contract_value_quote: Decimal,
    *,
    is_long: bool = True,
) -> Decimal:
    """Inverse contract PnL in base settlement currency."""
    _positive("entry", entry)
    _positive("exit", exit)
    _positive("contracts", contracts)
    _positive("contract_value_quote", contract_value_quote)
    if not isinstance(is_long, bool):
        raise ValueError("is_long must be bool")
    direction = Decimal(1) if is_long else Decimal(-1)
    return contracts * contract_value_quote * (Decimal(1) / entry - Decimal(1) / exit) * direction


def trading_fee(
    price: Decimal,
    quantity: Decimal,
    multiplier: Decimal,
    fee_rate: Decimal,
) -> Decimal:
    """Fee in the notional's quote currency, assuming a linear contract."""
    _positive("price", price)
    _positive("quantity", quantity)
    _positive("multiplier", multiplier)
    if not isinstance(fee_rate, Decimal) or not fee_rate.is_finite() or fee_rate < 0:
        raise ValueError("fee_rate must be a finite non-negative Decimal")
    return price * quantity * multiplier * fee_rate


def funding_cashflow(
    notional: Decimal,
    funding_rate: Decimal,
    *,
    is_long: bool,
) -> Decimal:
    """Cashflow sign convention: positive funding means longs pay shorts."""
    _positive("notional", notional)
    if not isinstance(funding_rate, Decimal) or not funding_rate.is_finite():
        raise ValueError("funding_rate must be a finite Decimal")
    if not isinstance(is_long, bool):
        raise ValueError("is_long must be bool")
    payment_to_position = notional * funding_rate
    return -payment_to_position if is_long else payment_to_position
