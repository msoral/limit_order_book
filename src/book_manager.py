from loguru import logger

import config
from src.book import Book
from src.data import Order
from src.limit import Limit
from src.orderbookentry import OrderBookEntry


class BookManager:
    def __init__(self, book: Book):
        self.book: Book = book
        self.step_size = 0.01

    def populate(self, orders: list[Order]) -> None:
        for order in orders:
            if order.message_type == 'A':  # add
                entry: OrderBookEntry = OrderBookEntry(order.order_id, order.size, order.price, True, order.time)
                self.book.add_order(entry)
            elif order.message_type == 'E':  # execute
                self.book.execute_order(order.order_id, order.size)
            else:  # delete
                self.book.delete_order(order.order_id)

    def show_order_book_limits(self) -> None:
        non_empty_limits = [limit for limit in self.book.buy_limits if limit.size != 0]
        order_book_display = f"Highest buy: {self.book.highest_buy} \n Lowest sell: {self.book.lowest_sell} \n" \
                             f"Positions: {non_empty_limits}"
        logger.info(order_book_display)

    def show_order_book_entries(self) -> None:
        non_empty_limits = [limit for limit in self.book.buy_limits if limit.size != 0]
        for limit in non_empty_limits:
            order = limit.head_order
            while order is not None:
                logger.debug(order)
                order = order.next_order

    def pre_allocate_with_boundaries(self, minimum: float, maximum: float) -> None:
        count = int((maximum - minimum) / self.step_size + 1)  # To include both boundaries add 1
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
            price: float = float(config.FLOAT_SIGNIFICANT_DIGIT_FORMAT.format(index * self.step_size + minimum))
            limit: Limit = Limit(price, index)
            self.book.buy_limits.append(limit)
            self.book.buy_price_limit_map[price] = limit

            self.book.sell_limits.append(limit)
            self.book.sell_price_limit_map[price] = limit
