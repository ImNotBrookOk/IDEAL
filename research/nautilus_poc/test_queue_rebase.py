"""L2 snapshot rebasing and L3 MBO queue tracking regression tests.

Synthetic fixtures isolate the pinned NautilusTrader 2.0.0rc9 simulator.
They are mechanism tests, not venue-matching parity claims.
"""
from decimal import Decimal

from nautilus_trader.backtest import BacktestEngine
from nautilus_trader.config import BacktestEngineConfig
from nautilus_trader.execution import MakerTakerFeeModel
from nautilus_trader.model import (
    AccountType,
    AggressorSide,
    BookAction,
    BookOrder,
    BookType,
    Currency,
    Money,
    OmsType,
    OrderBookDelta,
    OrderBookDeltas,
    OrderSide,
    Price,
    Quantity,
    QuoteTick,
    RecordFlag,
    TimeInForce,
    TradeId,
    TradeTick,
    Venue,
)
from nautilus_trader.testkit.providers import TestInstrumentProvider
from nautilus_trader.trading import Strategy


USDT = Currency.from_str("USDT")
INSTRUMENT = TestInstrumentProvider.btcusdt_perp_binance()
VENUE = Venue("BINANCE")
ASK = Price.from_str("40001.0")


class PassiveSellStrategy(Strategy):
    def __init__(self, quantity: str = "1.000"):
        super().__init__()
        self.quantity = Quantity.from_str(quantity)
        self.submitted = False
        self.order = None
        self.fill_events = []

    def on_start(self):
        self.subscribe_quotes(INSTRUMENT.id)

    def on_quote(self, quote):
        if self.submitted:
            return
        self.submitted = True
        self.order = self.order_factory.limit(
            instrument_id=INSTRUMENT.id,
            order_side=OrderSide.SELL,
            quantity=self.quantity,
            price=ASK,
            time_in_force=TimeInForce.GTC,
        )
        self.submit_order(self.order)

    def on_order_filled(self, event):
        self.fill_events.append(event)


def delta(action, side, price, size, order_id, sequence, flags=0):
    return OrderBookDelta(
        instrument_id=INSTRUMENT.id,
        action=action,
        order=BookOrder(
            side,
            Price.from_str(price),
            Quantity.from_str(size),
            order_id,
        ),
        flags=flags,
        sequence=sequence,
        ts_event=sequence,
        ts_init=sequence,
    )


def quote(timestamp: int = 2):
    return QuoteTick(
        instrument_id=INSTRUMENT.id,
        bid_price=Price.from_str("40000.0"),
        ask_price=ASK,
        bid_size=Quantity.from_str("10.000"),
        ask_size=Quantity.from_str("10.000"),
        ts_event=timestamp,
        ts_init=timestamp,
    )


def buy_trade(timestamp: int, size: str):
    return TradeTick(
        instrument_id=INSTRUMENT.id,
        price=ASK,
        size=Quantity.from_str(size),
        aggressor_side=AggressorSide.BUY,
        trade_id=TradeId(f"BUY-{timestamp}"),
        ts_event=timestamp,
        ts_init=timestamp,
    )


def make_engine(book_type: BookType, quantity: str = "1.000"):
    engine = BacktestEngine(
        BacktestEngineConfig(bypass_logging=True, run_analysis=False),
    )
    engine.add_venue(
        venue=VENUE,
        oms_type=OmsType.NETTING,
        account_type=AccountType.MARGIN,
        base_currency=USDT,
        starting_balances=[Money(100_000, USDT)],
        book_type=book_type,
        trade_execution=True,
        queue_position=True,
        liquidity_consumption=True,
        fee_model=MakerTakerFeeModel(
            maker_rate=Decimal("0"),
            taker_rate=Decimal("0"),
        ),
    )
    engine.add_instrument(INSTRUMENT)
    strategy = PassiveSellStrategy(quantity)
    engine.add_strategy(strategy)
    return engine, strategy


def run_l2_snapshot_case(snapshot_size: str, trade_size: str):
    engine, strategy = make_engine(BookType.L2_MBP)
    initial = OrderBookDeltas(
        INSTRUMENT.id,
        [
            delta(BookAction.ADD, OrderSide.BUY, "39999.0", "10.000", 0, 1),
            delta(
                BookAction.ADD,
                OrderSide.SELL,
                "40001.0",
                "10.000",
                0,
                1,
                RecordFlag.F_LAST.value,
            ),
        ],
    )
    replacement = OrderBookDeltas(
        INSTRUMENT.id,
        [
            OrderBookDelta.clear(INSTRUMENT.id, 3, 3, 3),
            delta(
                BookAction.ADD,
                OrderSide.SELL,
                "40001.0",
                snapshot_size,
                0,
                3,
                RecordFlag.F_LAST.value,
            ),
        ],
    )
    try:
        engine.add_data([initial, quote(), replacement, buy_trade(4, trade_size)])
        engine.run()
        return strategy.fill_events
    finally:
        engine.dispose()


def test_l2_snapshot_rebases_queue_down_to_new_visible_size():
    fills = run_l2_snapshot_case(snapshot_size="8.000", trade_size="9.000")

    # Original queue was 10. The replacement snapshot shows 8; a 9-unit
    # aggressive buy clears the rebased queue and fills exactly one unit.
    assert [event.last_qty for event in fills] == [Quantity.from_str("1.000")]


def test_l2_snapshot_does_not_push_existing_order_back_on_size_increase():
    fills = run_l2_snapshot_case(snapshot_size="15.000", trade_size="11.000")

    # Existing queue estimate remains capped at its prior 10; the extra 5
    # units in the replacement snapshot are not placed ahead of our order.
    assert [event.last_qty for event in fills] == [Quantity.from_str("1.000")]


def run_l3_case(book_updates, trade_size: str | list[str], order_quantity: str = "1.000"):
    engine, strategy = make_engine(BookType.L3_MBO, order_quantity)
    initial = OrderBookDeltas(
        INSTRUMENT.id,
        [
            delta(BookAction.ADD, OrderSide.BUY, "39999.0", "10.000", 900, 1),
            delta(BookAction.ADD, OrderSide.SELL, "40001.0", "5.000", 101, 1),
            delta(BookAction.ADD, OrderSide.SELL, "40001.0", "5.000", 102, 2),
        ],
    )
    try:
        data = [initial, quote(3)]
        data.extend(book_updates)
        trade_sizes = trade_size if isinstance(trade_size, list) else [trade_size]
        data.extend(buy_trade(10 + index, size) for index, size in enumerate(trade_sizes))
        engine.add_data(data)
        engine.run()
        return strategy.fill_events
    finally:
        engine.dispose()


def test_l3_delete_of_specific_order_ahead_advances_only_its_quantity():
    delete_first = delta(
        BookAction.DELETE,
        OrderSide.SELL,
        "40001.0",
        "5.000",
        101,
        4,
    )
    fills = run_l3_case([delete_first], trade_size="6.000")

    # The deleted 5-unit MBO order leaves 5 ahead. Six aggressive units
    # therefore permit exactly one unit to reach the simulated resting order.
    assert [event.last_qty for event in fills] == [Quantity.from_str("1.000")]


def test_l3_order_size_decrease_advances_queue_by_the_decrement():
    shrink_first = delta(
        BookAction.UPDATE,
        OrderSide.SELL,
        "40001.0",
        "3.000",
        101,
        4,
    )
    fills = run_l3_case([shrink_first], trade_size="9.000")

    # The first MBO order decreases from 5 to 3; queue ahead falls from 10 to 8.
    assert [event.last_qty for event in fills] == [Quantity.from_str("1.000")]


def test_l3_order_size_increase_adds_to_queue_ahead():
    grow_first = delta(
        BookAction.UPDATE,
        OrderSide.SELL,
        "40001.0",
        "7.000",
        101,
        4,
    )
    fills = run_l3_case([grow_first], trade_size="11.000")

    # NautilusTrader retains the order's FIFO slot and adds the 2-unit increase
    # to queue ahead: 12 ahead means 11 traded units cannot fill our order.
    assert fills == []


def test_l3_snapshot_rebase_preserves_existing_order_ids_not_new_orders():
    snapshot = OrderBookDeltas(
        INSTRUMENT.id,
        [
            OrderBookDelta.clear(INSTRUMENT.id, 4, 4, 4),
            delta(
                BookAction.ADD,
                OrderSide.SELL,
                "40001.0",
                "5.000",
                101,
                4,
                RecordFlag.F_SNAPSHOT.value,
            ),
            delta(
                BookAction.ADD,
                OrderSide.SELL,
                "40001.0",
                "5.000",
                102,
                4,
            ),
            delta(
                BookAction.ADD,
                OrderSide.SELL,
                "40001.0",
                "50.000",
                103,
                4,
                RecordFlag.F_LAST.value,
            ),
        ],
    )
    delete_first = delta(
        BookAction.DELETE,
        OrderSide.SELL,
        "40001.0",
        "5.000",
        101,
        5,
    )
    fills = run_l3_case([snapshot, delete_first], trade_size="6.000")

    # The simulated order originally queued behind IDs 101 and 102. The
    # replacement snapshot preserves those existing IDs, but the newly seen
    # ID 103 is not retroactively inserted ahead. Deleting ID 101 leaves 5
    # ahead, so six aggressive units fill exactly one.
    assert [event.last_qty for event in fills] == [Quantity.from_str("1.000")]



def test_l3_queue_partial_fills_are_bounded_by_trade_volume():
    fills = run_l3_case([], trade_size=["12.000", "3.000"], order_quantity="5.000")

    assert [event.last_qty for event in fills] == [
        Quantity.from_str("2.000"),
        Quantity.from_str("3.000"),
    ]
