"""Execution realism tests for partial fills, queueing, consumption and slippage.

These tests exercise the pinned NautilusTrader simulator only. They do not
claim exchange matching-engine parity.
"""

from decimal import Decimal

from nautilus_trader.backtest import BacktestEngine
from nautilus_trader.config import BacktestEngineConfig
from nautilus_trader.execution import DefaultFillModel, MakerTakerFeeModel
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


class LimitQueueStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.order_count = 1
        self.order_quantity = Quantity.from_str("1.000")
        self.submitted = False
        self.order_ids = []
        self.fill_events = []

    def on_start(self):
        self.subscribe_quotes(INSTRUMENT.id)

    def on_quote(self, quote):
        if self.submitted:
            return
        self.submitted = True
        for _ in range(self.order_count):
            order = self.order_factory.limit(
                instrument_id=INSTRUMENT.id,
                order_side=OrderSide.BUY,
                quantity=self.order_quantity,
                price=Price.from_str("40000.0"),
                time_in_force=TimeInForce.GTC,
            )
            self.order_ids.append(order.client_order_id)
            self.submit_order(order)

    def on_order_filled(self, event):
        self.fill_events.append(event)


class MarketBuyStrategy(Strategy):
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
                quantity=Quantity.from_str("1.000"),
            ),
        )

    def on_order_filled(self, event):
        self.fill_events.append(event)


def make_quote(timestamp: int) -> QuoteTick:
    return QuoteTick(
        instrument_id=INSTRUMENT.id,
        bid_price=Price.from_str("40000.0"),
        ask_price=Price.from_str("40001.0"),
        bid_size=Quantity.from_str("10.000"),
        ask_size=Quantity.from_str("10.000"),
        ts_event=timestamp,
        ts_init=timestamp,
    )


def make_sell_trade(timestamp: int, size: str) -> TradeTick:
    return TradeTick(
        instrument_id=INSTRUMENT.id,
        price=Price.from_str("40000.0"),
        size=Quantity.from_str(size),
        aggressor_side=AggressorSide.SELL,
        trade_id=TradeId(f"T-{timestamp}"),
        ts_event=timestamp,
        ts_init=timestamp,
    )


def build_engine(
    *,
    queue_position: bool = False,
    liquidity_consumption: bool = False,
    fill_model=None,
):
    engine = BacktestEngine(
        BacktestEngineConfig(bypass_logging=True, run_analysis=False),
    )
    engine.add_venue(
        venue=VENUE,
        oms_type=OmsType.NETTING,
        account_type=AccountType.MARGIN,
        base_currency=USDT,
        starting_balances=[Money(100_000, USDT)],
        book_type=BookType.L1_MBP,
        trade_execution=True,
        queue_position=queue_position,
        liquidity_consumption=liquidity_consumption,
        fee_model=MakerTakerFeeModel(
            maker_rate=Decimal("0"),
            taker_rate=Decimal("0"),
        ),
        fill_model=fill_model,
    )
    engine.add_instrument(INSTRUMENT)
    return engine


def run_limit_trade_case(
    *,
    order_count: int,
    order_quantity: str,
    trade_sizes: list[str],
    queue_position: bool,
    liquidity_consumption: bool,
):
    engine = build_engine(
        queue_position=queue_position,
        liquidity_consumption=liquidity_consumption,
    )
    strategy = LimitQueueStrategy()
    strategy.order_count = order_count
    strategy.order_quantity = Quantity.from_str(order_quantity)
    try:
        engine.add_strategy(strategy)
        data = [make_quote(1)]
        data.extend(
            make_sell_trade(index + 2, size)
            for index, size in enumerate(trade_sizes)
        )
        engine.add_data(data)
        engine.run()
        return strategy.fill_events, strategy.order_ids
    finally:
        engine.dispose()


def test_queue_position_requires_trade_volume_to_clear_displayed_quantity_ahead():
    fills, _ = run_limit_trade_case(
        order_count=1,
        order_quantity="5.000",
        trade_sizes=["12.000", "3.000"],
        queue_position=True,
        liquidity_consumption=True,
    )

    # 10 units are displayed ahead. The first 12-unit sell trade clears that
    # queue and fills only 2 units; the next trade fills the remaining 3.
    assert [event.last_qty for event in fills] == [
        Quantity.from_str("2.000"),
        Quantity.from_str("3.000"),
    ]


def test_competing_limit_orders_share_one_trade_budget_when_consumption_enabled():
    fills, _ = run_limit_trade_case(
        order_count=2,
        order_quantity="2.000",
        trade_sizes=["3.000"],
        queue_position=False,
        liquidity_consumption=True,
    )

    # The same 3-unit print cannot fill two 2-unit orders in aggregate.
    total_filled = sum((Decimal(str(event.last_qty)) for event in fills), Decimal("0"))
    assert total_filled == Decimal("3.000")


def test_l1_market_order_slippage_is_one_adverse_tick_when_probability_is_one():
    fill_model = DefaultFillModel(
        prob_fill_on_limit=1.0,
        prob_slippage=1.0,
        random_seed=42,
    )
    engine = build_engine(fill_model=fill_model)
    strategy = MarketBuyStrategy()
    try:
        engine.add_strategy(strategy)
        engine.add_data([make_quote(1)])
        engine.run()

        assert len(strategy.fill_events) == 1
        assert strategy.fill_events[0].last_px == Price.from_str("40001.1")
    finally:
        engine.dispose()



class L2MarketBuyStrategy(Strategy):
    def __init__(self, quantities: list[str]):
        super().__init__()
        self.quantities = quantities
        self.fill_events = []
        self.submitted = False

    def on_start(self):
        self.subscribe_quotes(INSTRUMENT.id)

    def on_quote(self, quote):
        if self.submitted:
            return
        self.submitted = True
        for quantity in self.quantities:
            self.submit_order(
                self.order_factory.market(
                    instrument_id=INSTRUMENT.id,
                    order_side=OrderSide.BUY,
                    quantity=Quantity.from_str(quantity),
                ),
            )

    def on_order_filled(self, event):
        self.fill_events.append(event)


def make_l2_book(timestamp: int = 1):
    """Create a two-sided L2 MBP book with two ask levels."""
    deltas = []
    entries = [
        (OrderSide.BUY, "39999.0", "2.000"),
        (OrderSide.SELL, "40001.0", "0.400"),
        (OrderSide.SELL, "40002.0", "0.600"),
    ]
    for index, (side, price, size) in enumerate(entries):
        sequence = index + 1
        flags = RecordFlag.F_LAST.value if index == len(entries) - 1 else 0
        deltas.append(
            OrderBookDelta(
                instrument_id=INSTRUMENT.id,
                action=BookAction.ADD,
                order=BookOrder(
                    side,
                    Price.from_str(price),
                    Quantity.from_str(size),
                    sequence,
                ),
                flags=flags,
                sequence=sequence,
                ts_event=timestamp,
                ts_init=timestamp,
            ),
        )
    return OrderBookDeltas(INSTRUMENT.id, deltas)


def run_l2_market_case(quantities: list[str]):
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
        trade_execution=True,
        liquidity_consumption=True,
        fee_model=MakerTakerFeeModel(
            maker_rate=Decimal("0"),
            taker_rate=Decimal("0"),
        ),
    )
    engine.add_instrument(INSTRUMENT)
    strategy = L2MarketBuyStrategy(quantities)
    try:
        engine.add_strategy(strategy)
        engine.add_data([make_l2_book(), make_quote(2)])
        engine.run()
        return strategy.fill_events
    finally:
        engine.dispose()


def test_l2_market_order_walks_multiple_ask_levels_and_partially_fills():
    fills = run_l2_market_case(["1.500"])

    assert [event.last_qty for event in fills] == [
        Quantity.from_str("0.400"),
        Quantity.from_str("0.600"),
    ]
    assert [event.last_px for event in fills] == [
        Price.from_str("40001.0"),
        Price.from_str("40002.0"),
    ]


def test_competing_l2_market_orders_cannot_reuse_consumed_depth():
    fills = run_l2_market_case(["0.750", "0.750"])

    total_filled = sum(
        (Decimal(str(event.last_qty)) for event in fills),
        Decimal("0"),
    )
    assert total_filled == Decimal("1.000")
