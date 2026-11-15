from decimal import Decimal

import pytest

from nautilus_trader.backtest import BacktestEngine
from nautilus_trader.config import BacktestEngineConfig
from nautilus_trader.execution import MakerTakerFeeModel
from nautilus_trader.model import (
    AccountType,
    BookAction,
    BookOrder,
    BookType,
    CryptoPerpetual,
    Currency,
    InstrumentId,
    FundingRateUpdate,
    MarkPriceUpdate,
    Money,
    OmsType,
    OrderBookDelta,
    OrderBookDeltas,
    OrderSide,
    Price,
    Quantity,
    QuoteTick,
    RecordFlag,
    Symbol,
    TimeInForce,
    Venue,
)
from nautilus_trader.testkit.providers import TestInstrumentProvider
from nautilus_trader.trading import Strategy


INSTRUMENT = CryptoPerpetual(
    instrument_id=InstrumentId.from_str("BTCJPY-PERP.BYBIT"),
    raw_symbol=Symbol("BTCJPY"),
    base_currency=Currency.from_str("BTC"),
    quote_currency=Currency.from_str("JPY"),
    settlement_currency=Currency.from_str("BTC"),
    is_inverse=True,
    price_precision=1,
    size_precision=0,
    price_increment=Price.from_str("0.5"),
    size_increment=Quantity.from_str("1"),
    ts_event=0,
    ts_init=0,
    max_notional=Money(10_000_000.0, Currency.from_str("JPY")),
    min_notional=Money(1.0, Currency.from_str("JPY")),
    max_price=Price.from_str("100000000.0"),
    min_price=Price.from_str("0.5"),
    margin_init=Decimal("0.01"),
    margin_maint=Decimal("0.0035"),
)
BTCUSD_INSTRUMENT = TestInstrumentProvider.default_fx_ccy("BTCUSD", Venue("BYBIT"))
TRIGGER_INSTRUMENT = TestInstrumentProvider.default_fx_ccy("ETHUSD", Venue("BYBIT"))
VENUE = Venue("BYBIT")
USD = Currency.from_str("USD")
BASE_NS = 1_700_000_000_000_000_000


class OpenInverseLong(Strategy):
    def __init__(self):
        super().__init__()
        self.submitted = False
        self.fills = []

    def on_start(self):
        # Trigger the BTCJPY order from a different instrument so no BTC/JPY
        # quote is cached for later funding conversion.
        self.subscribe_quotes(TRIGGER_INSTRUMENT.id)

    def on_quote(self, quote):
        if self.submitted:
            return
        self.submitted = True
        self.submit_order(
            self.order_factory.limit(
                instrument_id=INSTRUMENT.id,
                order_side=OrderSide.BUY,
                quantity=Quantity.from_str("1000"),
                price=Price.from_str("6000000.0"),
                time_in_force=TimeInForce.GTC,
            ),
        )

    def on_order_filled(self, event):
        self.fills.append(event)
        if event.instrument_id == INSTRUMENT.id:
            # BTC/USD permits entry risk validation. Remove it after entry so
            # the later funding settlement has no conversion path.
            self.cache.purge_instrument(BTCUSD_INSTRUMENT.id)


def btcjpy_book(timestamp: int):
    return OrderBookDeltas(
        INSTRUMENT.id,
        [
            OrderBookDelta(
                instrument_id=INSTRUMENT.id,
                action=BookAction.ADD,
                order=BookOrder(
                    OrderSide.BUY,
                    Price.from_str("5999999.5"),
                    Quantity.from_str("5000"),
                    1,
                ),
                flags=0,
                sequence=1,
                ts_event=timestamp,
                ts_init=timestamp,
            ),
            OrderBookDelta(
                instrument_id=INSTRUMENT.id,
                action=BookAction.ADD,
                order=BookOrder(
                    OrderSide.SELL,
                    Price.from_str("6000000.0"),
                    Quantity.from_str("5000"),
                    2,
                ),
                flags=RecordFlag.F_LAST.value,
                sequence=2,
                ts_event=timestamp,
                ts_init=timestamp,
            ),
        ],
    )


def clear_btcjpy_book(timestamp: int):
    return OrderBookDeltas(
        INSTRUMENT.id,
        [
            OrderBookDelta(
                instrument_id=INSTRUMENT.id,
                action=BookAction.CLEAR,
                order=BookOrder(
                    OrderSide.BUY,
                    Price.from_str("5999999.5"),
                    Quantity.from_str("0"),
                    0,
                ),
                flags=0,
                sequence=3,
                ts_event=timestamp,
                ts_init=timestamp,
            ),
            OrderBookDelta(
                instrument_id=INSTRUMENT.id,
                action=BookAction.CLEAR,
                order=BookOrder(
                    OrderSide.SELL,
                    Price.from_str("6000000.0"),
                    Quantity.from_str("0"),
                    0,
                ),
                flags=RecordFlag.F_LAST.value,
                sequence=4,
                ts_event=timestamp,
                ts_init=timestamp,
            ),
        ],
    )




def btcusd_spot_book(timestamp: int):
    return OrderBookDeltas(
        BTCUSD_INSTRUMENT.id,
        [
            OrderBookDelta(
                instrument_id=BTCUSD_INSTRUMENT.id,
                action=BookAction.ADD,
                order=BookOrder(
                    OrderSide.BUY,
                    Price.from_str("39999.90000"),
                    Quantity.from_str("100000"),
                    21,
                ),
                flags=0,
                sequence=1,
                ts_event=timestamp,
                ts_init=timestamp,
            ),
            OrderBookDelta(
                instrument_id=BTCUSD_INSTRUMENT.id,
                action=BookAction.ADD,
                order=BookOrder(
                    OrderSide.SELL,
                    Price.from_str("40000.00000"),
                    Quantity.from_str("100000"),
                    22,
                ),
                flags=RecordFlag.F_LAST.value,
                sequence=2,
                ts_event=timestamp,
                ts_init=timestamp,
            ),
        ],
    )


def btcusd_spot_quote(timestamp: int):
    return QuoteTick(
        instrument_id=BTCUSD_INSTRUMENT.id,
        bid_price=Price.from_str("39999.90000"),
        ask_price=Price.from_str("40000.00000"),
        bid_size=Quantity.from_str("100000"),
        ask_size=Quantity.from_str("100000"),
        ts_event=timestamp,
        ts_init=timestamp,
    )

def trigger_book(timestamp: int):
    return OrderBookDeltas(
        TRIGGER_INSTRUMENT.id,
        [
            OrderBookDelta(
                instrument_id=TRIGGER_INSTRUMENT.id,
                action=BookAction.ADD,
                order=BookOrder(
                    OrderSide.BUY,
                    Price.from_str("2999.90000"),
                    Quantity.from_str("100000"),
                    11,
                ),
                flags=0,
                sequence=1,
                ts_event=timestamp,
                ts_init=timestamp,
            ),
            OrderBookDelta(
                instrument_id=TRIGGER_INSTRUMENT.id,
                action=BookAction.ADD,
                order=BookOrder(
                    OrderSide.SELL,
                    Price.from_str("3000.00000"),
                    Quantity.from_str("100000"),
                    12,
                ),
                flags=RecordFlag.F_LAST.value,
                sequence=2,
                ts_event=timestamp,
                ts_init=timestamp,
            ),
        ],
    )

def trigger_quote(timestamp: int):
    return QuoteTick(
        instrument_id=TRIGGER_INSTRUMENT.id,
        bid_price=Price.from_str("2999.90000"),
        ask_price=Price.from_str("3000.00000"),
        bid_size=Quantity.from_str("100000"),
        ask_size=Quantity.from_str("100000"),
        ts_event=timestamp,
        ts_init=timestamp,
    )


def run_missing_fx_conversion():
    engine = BacktestEngine(
        BacktestEngineConfig(bypass_logging=True, run_analysis=False),
    )
    engine.add_venue(
        venue=VENUE,
        oms_type=OmsType.NETTING,
        account_type=AccountType.MARGIN,
        starting_balances=[Money.from_str("100000 USD")],
        base_currency=USD,
        book_type=BookType.L2_MBP,
        trade_execution=False,
        liquidity_consumption=True,
        fee_model=MakerTakerFeeModel(
            maker_rate=Decimal("0"),
            taker_rate=Decimal("0"),
        ),
    )
    engine.add_instrument(INSTRUMENT)
    engine.add_instrument(BTCUSD_INSTRUMENT)
    engine.add_instrument(TRIGGER_INSTRUMENT)
    strategy = OpenInverseLong()
    try:
        engine.add_strategy(strategy)
        mark_ts = BASE_NS + 3_000_000_000
        funding_ts = BASE_NS + 3_100_000_000
        boundary = BASE_NS + 4_000_000_000
        engine.add_data([
            btcjpy_book(BASE_NS + 1_000_000_000),
            btcusd_spot_book(BASE_NS + 1_200_000_000),
            trigger_book(BASE_NS + 1_500_000_000),
            btcusd_spot_quote(BASE_NS + 1_800_000_000),
            trigger_quote(BASE_NS + 2_000_000_000),
            MarkPriceUpdate(
                instrument_id=INSTRUMENT.id,
                value=Price.from_str("6000000.0"),
                ts_event=mark_ts,
                ts_init=mark_ts,
            ),
            FundingRateUpdate(
                instrument_id=INSTRUMENT.id,
                rate=Decimal("0.0001"),
                ts_event=funding_ts,
                ts_init=funding_ts,
                interval=480,
                next_funding_ns=boundary,
            ),
            clear_btcjpy_book(BASE_NS + 3_500_000_000),
            # Advance beyond the boundary so the engine actually attempts settlement.
            trigger_quote(BASE_NS + 5_000_000_000),
        ])
        with pytest.raises(RuntimeError, match="Funding settlement failed"):
            engine.run()
        return {
            "fills": list(strategy.fills),
            "open_positions": engine.cache.positions_open_count(),
        }
    finally:
        engine.dispose()


def test_inverse_funding_with_missing_btc_to_usd_conversion_fails_closed():
    result = run_missing_fx_conversion()

    assert len(result["fills"]) == 1
    assert result["open_positions"] == 1
