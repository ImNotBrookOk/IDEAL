from decimal import Decimal

from nautilus_trader.backtest import BacktestEngine
from nautilus_trader.config import BacktestEngineConfig
from nautilus_trader.execution import MakerTakerFeeModel
from nautilus_trader.model import (
    AccountType,
    BookType,
    Currency,
    FundingRateUpdate,
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


INSTRUMENT = TestInstrumentProvider.btcusdt_perp_binance()
VENUE = Venue("SIM")
USDT = Currency.from_str("USDT")
BASE_NS = 1_700_000_000_000_000_000


def make_quote(offset: int) -> QuoteTick:
    timestamp = BASE_NS + offset
    return QuoteTick(
        instrument_id=INSTRUMENT.id,
        bid_price=Price.from_str("60000.00"),
        ask_price=Price.from_str("60000.50"),
        bid_size=Quantity.from_str("1.000"),
        ask_size=Quantity.from_str("1.000"),
        ts_event=timestamp,
        ts_init=timestamp,
    )


class OpenTwoLongs(Strategy):
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
        for _ in range(2):
            self.submit_order(
                self.order_factory.market(
                    instrument_id=INSTRUMENT.id,
                    order_side=OrderSide.BUY,
                    quantity=Quantity.from_str("0.100"),
                ),
            )

    def on_order_filled(self, event):
        self.fills.append(event)


def funding_update(ts: int, boundary: int) -> FundingRateUpdate:
    return FundingRateUpdate(
        instrument_id=INSTRUMENT.id,
        rate=Decimal("0.0001"),
        ts_event=ts,
        ts_init=ts,
        interval=480,
        next_funding_ns=boundary,
    )


def run_two_position_funding(*, duplicate_after_boundary: bool):
    engine = BacktestEngine(
        BacktestEngineConfig(bypass_logging=True, run_analysis=False),
    )
    engine.add_venue(
        venue=VENUE,
        oms_type=OmsType.HEDGING,
        account_type=AccountType.MARGIN,
        starting_balances=[Money.from_str("10000 USDT")],
        book_type=BookType.L1_MBP,
        fee_model=MakerTakerFeeModel(
            maker_rate=Decimal("0.0002"),
            taker_rate=Decimal("0.0005"),
        ),
        liquidity_consumption=True,
        use_market_order_acks=True,
    )
    engine.add_instrument(INSTRUMENT)
    strategy = OpenTwoLongs()
    try:
        engine.add_strategy(strategy)
        boundary = BASE_NS + 3_000_000_000
        data = [
            make_quote(1_000_000_000),
            funding_update(BASE_NS + 2_600_000_000, boundary),
        ]
        if duplicate_after_boundary:
            data.append(funding_update(BASE_NS + 3_500_000_000, boundary))
        data.append(make_quote(4_000_000_000))
        engine.add_data(data)
        engine.run()
        account = engine.portfolio.account(venue=VENUE)
        return {
            "fill_count": len(strategy.fills),
            "open_positions": engine.cache.positions_open_count(),
            "balance": account.balance_total(USDT),
        }
    finally:
        engine.dispose()


def test_funding_falls_back_to_top_of_book_mid_when_mark_is_missing():
    result = run_two_position_funding(duplicate_after_boundary=False)

    assert result["fill_count"] == 2
    assert result["open_positions"] == 2
    # Each 0.1 BTC position is valued at the 60,000.25 bid/ask midpoint.
    # Funding debit per position: 6,000.025 * 0.0001 = 0.6000025 USDT.
    # Two taker fees: 2 * 3.000025 USDT.
    assert result["balance"] == Money.from_str("9992.79994500 USDT")


def test_repeated_funding_update_after_settlement_is_idempotent():
    once = run_two_position_funding(duplicate_after_boundary=False)
    repeated = run_two_position_funding(duplicate_after_boundary=True)

    assert repeated == once
