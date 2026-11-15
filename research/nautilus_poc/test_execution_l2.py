"""L2 depth-walking and competing-liquidity tests for the pinned POC."""

from decimal import Decimal

from nautilus_trader.backtest import BacktestEngine
from nautilus_trader.config import BacktestEngineConfig
from nautilus_trader.execution import MakerTakerFeeModel
from nautilus_trader.model import (
    AccountType,
    BookAction,
    BookOrder,
    BookType,
    Currency,
    Money,
    OrderBookDelta,
    OrderBookDeltas,
    OrderSide,
    OmsType,
    Price,
    Quantity,
    QuoteTick,
    RecordFlag,
    Venue,
)
from nautilus_trader.testkit.providers import TestInstrumentProvider
from nautilus_trader.trading import Strategy


USDT = Currency.from_str("USDT")
INSTRUMENT = TestInstrumentProvider.btcusdt_perp_binance()
VENUE = Venue("BINANCE")


class L2MarketBuyStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.submitted = False
        self.order_ids = []
        self.fill_events = []

    def on_start(self):
        self.subscribe_quotes(INSTRUMENT.id)

    def on_quote(self, quote):
        if self.submitted:
            return
        self.submitted = True
        for _ in range(2):
            order = self.order_factory.market(
                instrument_id=INSTRUMENT.id,
                order_side=OrderSide.BUY,
                quantity=Quantity.from_str("3.000"),
            )
            self.order_ids.append(order.client_order_id)
            self.submit_order(order)

    def on_order_filled(self, event):
        self.fill_events.append(event)


def make_quote() -> QuoteTick:
    return QuoteTick(
        instrument_id=INSTRUMENT.id,
        bid_price=Price.from_str("39999.0"),
        ask_price=Price.from_str("40001.0"),
        bid_size=Quantity.from_str("5.000"),
        ask_size=Quantity.from_str("2.000"),
        ts_event=2,
        ts_init=2,
    )


def make_l2_snapshot() -> OrderBookDeltas:
    instrument_id = INSTRUMENT.id
    timestamp = 1
    sequence = 1
    return OrderBookDeltas(
        instrument_id,
        [
            OrderBookDelta.clear(instrument_id, sequence, timestamp, timestamp),
            OrderBookDelta(
                instrument_id=instrument_id,
                action=BookAction.ADD,
                order=BookOrder(
                    OrderSide.BUY,
                    Price.from_str("39999.0"),
                    Quantity.from_str("5.000"),
                    1,
                ),
                flags=0,
                sequence=sequence,
                ts_event=timestamp,
                ts_init=timestamp,
            ),
            OrderBookDelta(
                instrument_id=instrument_id,
                action=BookAction.ADD,
                order=BookOrder(
                    OrderSide.SELL,
                    Price.from_str("40001.0"),
                    Quantity.from_str("2.000"),
                    2,
                ),
                flags=0,
                sequence=sequence,
                ts_event=timestamp,
                ts_init=timestamp,
            ),
            OrderBookDelta(
                instrument_id=instrument_id,
                action=BookAction.ADD,
                order=BookOrder(
                    OrderSide.SELL,
                    Price.from_str("40002.0"),
                    Quantity.from_str("3.000"),
                    3,
                ),
                flags=RecordFlag.F_SNAPSHOT.value | RecordFlag.F_LAST.value,
                sequence=sequence,
                ts_event=timestamp,
                ts_init=timestamp,
            ),
        ],
    )


def test_l2_depth_walk_and_consumption_prevent_competing_orders_reusing_depth():
    engine = BacktestEngine(
        BacktestEngineConfig(bypass_logging=True, run_analysis=False),
    )
    engine.add_venue(
        venue=VENUE,
        oms_type=OmsType.NETTING,
        account_type=AccountType.MARGIN,
        base_currency=USDT,
        starting_balances=[Money(100_000, USDT)],
        book_type=BookType.L2_MBP,
        trade_execution=False,
        liquidity_consumption=True,
        fee_model=MakerTakerFeeModel(
            maker_rate=Decimal("0"),
            taker_rate=Decimal("0"),
        ),
    )
    engine.add_instrument(INSTRUMENT)
    strategy = L2MarketBuyStrategy()
    try:
        engine.add_strategy(strategy)
        engine.add_data([make_l2_snapshot(), make_quote()])
        engine.run()

        filled_by_order = {}
        filled_by_price = {}
        for event in strategy.fill_events:
            filled_by_order[event.client_order_id] = (
                filled_by_order.get(event.client_order_id, Decimal("0"))
                + Decimal(str(event.last_qty))
            )
            filled_by_price[event.last_px] = (
                filled_by_price.get(event.last_px, Decimal("0"))
                + Decimal(str(event.last_qty))
            )

        assert filled_by_order[strategy.order_ids[0]] == Decimal("3.000")
        assert filled_by_order[strategy.order_ids[1]] == Decimal("2.000")
        assert filled_by_price[Price.from_str("40001.0")] == Decimal("2.000")
        assert filled_by_price[Price.from_str("40002.0")] == Decimal("3.000")
    finally:
        engine.dispose()
