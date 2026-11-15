"""Research-only test for cross-currency collateral liquidation boundaries.

The fixture deliberately gives a USDT-settled linear perpetual a large BTC balance
but insufficient USDT equity after an adverse move. It records whether the pinned
simulator treats BTC as cross-collateral for the USDT-settled position.
"""

from decimal import Decimal

from nautilus_trader.backtest import BacktestEngine
from nautilus_trader.config import BacktestEngineConfig
from nautilus_trader.execution import MakerTakerFeeModel
from nautilus_trader.model import (
    AccountType,
    BookType,
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
USDT = Currency.from_str("USDT")
VENUE = Venue("BINANCE")
INSTRUMENT = TestInstrumentProvider.btcusdt_perp_binance()
BASE_NS = 1_700_000_000_000_000_000


def make_quote(bid: str, ask: str, offset: int) -> QuoteTick:
    timestamp = BASE_NS + offset
    return QuoteTick(
        instrument_id=INSTRUMENT.id,
        bid_price=Price.from_str(bid),
        ask_price=Price.from_str(ask),
        bid_size=Quantity.from_str("0.100"),
        ask_size=Quantity.from_str("0.100"),
        ts_event=timestamp,
        ts_init=timestamp,
    )


class OpenLinearLong(Strategy):
    def __init__(self):
        super().__init__()
        self.submitted = False
        self.fills = []

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
                quantity=Quantity.from_str("0.100"),
            ),
        )

    def on_order_filled(self, event):
        self.fills.append(event)


def run_btc_collateral_vs_usdt_liquidation_case():
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
        liquidation_enabled=True,
        liquidation_trigger_ratio=1.0,
        liquidation_cancel_open_orders=True,
    )
    engine.add_instrument(INSTRUMENT)
    strategy = OpenLinearLong()

    try:
        engine.add_strategy(strategy)
        engine.add_data([
            # The market buy executes at the 60,000 ask.
            make_quote("59999.5", "60000.0", 1_000_000_000),
            # A 10,000 adverse move loses 1,000 USDT on 0.1 BTC.
            make_quote("49999.5", "50000.0", 2_000_000_000),
        ])
        engine.run()
        account = engine.portfolio.account(venue=VENUE)
        return {
            "base_currency": account.base_currency,
            "btc_balance": account.balance_total(BTC),
            "usdt_balance": account.balance_total(USDT),
            "open_positions": engine.cache.positions_open_count(),
            "closed_positions": engine.cache.positions_closed_count(),
            "fill_count": len(strategy.fills),
        }
    finally:
        engine.dispose()


def test_btc_balance_does_not_offset_usdt_settled_liquidation_in_simulator():
    result = run_btc_collateral_vs_usdt_liquidation_case()

    # The account owns 2 BTC of collateral, but this pinned simulator's
    # liquidation check is bucketed by each position's settlement currency.
    # The 0.1 BTCUSDT loss exhausts the 1,000 USDT balance and triggers closure.
    assert result["base_currency"] is None
    assert result["btc_balance"] == Money.from_str("2 BTC")
    assert result["usdt_balance"] == Money.from_str("0 USDT")
    assert result["open_positions"] == 0
    assert result["closed_positions"] == 1
    assert result["fill_count"] == 2


def test_btc_collateral_liquidation_replay_is_deterministic():
    assert (
        run_btc_collateral_vs_usdt_liquidation_case()
        == run_btc_collateral_vs_usdt_liquidation_case()
    )
