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


def make_quote(offset: int) -> QuoteTick:
    timestamp = BASE_NS + offset
    return QuoteTick(
        instrument_id=INSTRUMENT_ID,
        bid_price=Price.from_str("60000.00"),
        ask_price=Price.from_str("60000.50"),
        bid_size=Quantity.from_str("1.000"),
        ask_size=Quantity.from_str("1.000"),
        ts_event=timestamp,
        ts_init=timestamp,
    )


class OpenOneLong(Strategy):
    def __init__(self):
        super().__init__()
        self.submitted = False
        self.fill_count = 0
        self.fills = []

    def on_start(self):
        self.subscribe_quotes(INSTRUMENT_ID)

    def on_quote(self, quote):
        if self.submitted:
            return
        self.submitted = True
        self.submit_order(
            self.order_factory.market(
                instrument_id=INSTRUMENT_ID,
                order_side=OrderSide.BUY,
                quantity=Quantity.from_str("0.100"),
            ),
        )

    def on_order_filled(self, event):
        self.fill_count += 1
        self.fills.append(event)


def run_funding_case():
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
        use_market_order_acks=True,
    )
    engine.add_instrument(make_instrument())
    strategy = OpenOneLong()
    try:
        engine.add_strategy(strategy)
        mark_ts = BASE_NS + 2_500_000_000
        funding_ts = BASE_NS + 2_600_000_000
        settlement_ts = BASE_NS + 3_000_000_000
        engine.add_data([
            make_quote(1_000_000_000),
            MarkPriceUpdate(
                instrument_id=INSTRUMENT_ID,
                value=Price.from_str("60000.50"),
                ts_event=mark_ts,
                ts_init=mark_ts,
            ),
            FundingRateUpdate(
                instrument_id=INSTRUMENT_ID,
                rate=Decimal("0.0001"),
                ts_event=funding_ts,
                ts_init=funding_ts,
                interval=480,
                next_funding_ns=settlement_ts,
            ),
            make_quote(4_000_000_000),
        ])
        engine.run()
        account = engine.portfolio.account(venue=Venue("SIM"))
        return {
            "fill_count": strategy.fill_count,
            "commission": strategy.fills[0].commission,
            "open_positions": engine.cache.positions_open_count(),
            "balance": account.balance_total(USDT),
        }
    finally:
        engine.dispose()


def test_positive_funding_settles_at_next_funding_boundary():
    result = run_funding_case()
    assert result["fill_count"] == 1
    assert result["open_positions"] == 1
    assert result["commission"] == Money.from_str("3.00002500 USDT")
    # $6,000.05 notional * 0.0001 = $0.600005 funding debit.
    # The taker fee is $3.000025, leaving $9,996.399970.
    assert result["balance"] == Money.from_str("9996.39997000 USDT")


def test_funding_settlement_replay_is_deterministic():
    assert run_funding_case() == run_funding_case()



def run_without_funding_boundary():
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
        use_market_order_acks=True,
    )
    engine.add_instrument(make_instrument())
    strategy = OpenOneLong()
    try:
        engine.add_strategy(strategy)
        update_ts = BASE_NS + 2_600_000_000
        engine.add_data([
            make_quote(1_000_000_000),
            MarkPriceUpdate(
                instrument_id=INSTRUMENT_ID,
                value=Price.from_str("60000.50"),
                ts_event=BASE_NS + 2_500_000_000,
                ts_init=BASE_NS + 2_500_000_000,
            ),
            FundingRateUpdate(
                instrument_id=INSTRUMENT_ID,
                rate=Decimal("0.0001"),
                ts_event=update_ts,
                ts_init=update_ts,
                interval=480,
                next_funding_ns=None,
            ),
            make_quote(4_000_000_000),
        ])
        engine.run()
        account = engine.portfolio.account(venue=Venue("SIM"))
        return account.balance_total(USDT)
    finally:
        engine.dispose()


def test_funding_update_without_a_valid_boundary_does_not_settle():
    assert run_without_funding_boundary() == Money.from_str("9996.99997500 USDT")
