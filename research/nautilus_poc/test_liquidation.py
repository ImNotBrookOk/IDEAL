"""Liquidation behaviour tests for the isolated NautilusTrader POC."""

from decimal import Decimal

from nautilus_trader.backtest import BacktestEngine
from nautilus_trader.config import BacktestEngineConfig
from nautilus_trader.execution import MakerTakerFeeModel
from nautilus_trader.model import (
    AccountType,
    Currency,
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


class BuyInverseOnce(Strategy):
    def __init__(self):
        super().__init__()
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
                order_side=OrderSide.BUY,
                quantity=Quantity.from_int(10_000_000),
            ),
        )

    def on_order_filled(self, event):
        self.fill_events.append(event)


def make_quote(price: int, timestamp: int) -> QuoteTick:
    value = Price.from_int(price)
    return QuoteTick(
        instrument_id=INSTRUMENT.id,
        bid_price=value,
        ask_price=value,
        bid_size=Quantity.from_int(10_000_000),
        ask_size=Quantity.from_int(10_000_000),
        ts_event=timestamp,
        ts_init=timestamp,
    )


def run_liquidation_case():
    engine = BacktestEngine(
        BacktestEngineConfig(bypass_logging=True, run_analysis=False),
    )
    strategy = BuyInverseOnce()
    try:
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
