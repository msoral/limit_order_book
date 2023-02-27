from src.book import Book
from src.data import Order
from src.limit import Limit
from src.orderbookentry import OrderBookEntry
from src.utils.performance import measure_time_ns


class BookManager:
    def __init__(self, book: Book):
        self.book = book
        self.step_size = 0.01

    @measure_time_ns
    def populate(self, orders: list[Order]) -> None:
        for order in orders:
            if order.message_type == 'A':  # add
                entry: OrderBookEntry = OrderBookEntry(order.order_id, order.size, order.price, True, order.time)
                self.book.add_order(entry)
            elif order.message_type == 'E':  # execute
                self.book.execute_order(order.order_id)
            else:  # delete
                self.book.delete_order(order.order_id)

    def pre_allocate_with_boundaries(self, minimum: float, maximum: float) -> None:
        count = int((maximum - minimum) / self.step_size)
        self.__pre_allocate_limit_lists(minimum, count)

    def pre_allocate_with_threshold(self, closing_price: float, change_threshold: float) -> None:
        delta = closing_price * change_threshold
        minimum = closing_price - delta
        maximum = closing_price + delta
        count = int((maximum - minimum) / self.step_size)
        self.__pre_allocate_limit_lists(minimum, count)

    def __pre_allocate_limit_lists(self, minimum: float, count: int):
        # Speed of this operation does not matter because it can be done before the market opens.
        # If pre allocation speed is a concern using list comprehension should be considered.
        for index in range(count):
            price: float = minimum + (index * self.step_size)
            limit: Limit = Limit(price, index)
            self.book.buy_limits.append(limit)
            self.book.buy_price_limit_map[price] = limit

            self.book.sell_limits.append(limit)
            self.book.sell_price_limit_map[price] = limit
