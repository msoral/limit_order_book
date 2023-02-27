import uuid
from dataclasses import dataclass, field

import config
from limit import Limit
from src.orderbookentry import OrderBookEntry


@dataclass(slots=True)
class Book:
    buy_limits: list[Limit] = field(default_factory=list)
    sell_limits: list[Limit] = field(default_factory=list)
    lowest_sell: Limit = field(init=False)
    highest_buy: Limit = field(init=False)
    order_id_map: dict[uuid, OrderBookEntry] = field(default_factory=dict, repr=False, compare=False)
    sell_price_limit_map: dict[float, Limit] = field(default_factory=dict, repr=False, compare=False)
    buy_price_limit_map: dict[float, Limit] = field(default_factory=dict, repr=False, compare=False)

    def add_order(self, order: OrderBookEntry) -> None:
        if order.is_buy:
            self.__add_buy_order(order)
        else:
            self.__add_sell_order(order)

    def __add_buy_order(self, order: OrderBookEntry):
        limit = self.buy_price_limit_map.get(order.price)
        if limit is None:
            if self.buy_limits[0].price > order.price:
                for item in self.buy_limits:
                    item.position += 1
                limit = Limit(order.price, 0)
                self.buy_limits.insert(0, limit)
            else:
                limit = Limit(order.price, len(self.buy_limits))
                self.buy_limits.append(limit)
        else:
            limit.add(order)

        if self.highest_buy is None or limit.price > self.highest_buy.price:
            self.highest_buy = limit

    def __add_sell_order(self, order: OrderBookEntry):
        limit = self.sell_price_limit_map.get(order.price)
        if limit is None:
            if self.sell_limits[0].price > order.price:
                for item in self.sell_limits:
                    item.position += 1
                limit = Limit(order.price, 0)
                self.sell_limits.insert(0, limit)
            else:
                limit = Limit(order.price, len(self.sell_limits))
                self.sell_limits.append(limit)
        else:
            limit.add(order)

        if self.lowest_sell is None or limit.price < self.lowest_sell.price:
            self.lowest_sell = limit

    def delete_order(self, order_id: uuid) -> None:
        order = self.order_id_map.pop(order_id)
        order.limit.remove(order)
        del order

    def execute_order(self, order_id: uuid) -> None:
        order = self.order_id_map.pop(order_id)
        order.limit.execute(order)
        del order

    def get_top_of_the_book(self) -> dict[float, int]:
        best_bid: Limit = self.highest_buy
        result: dict[float, int] = {}
        if best_bid is None:
            return result

        for index in range(best_bid.position, best_bid.position + config.TOP_OF_THE_BOOK_PRICE_COUNT):
            limit = self.buy_limits[index]
            result[limit.price] = limit.size

        return result

    def get_queue_position(self, unique_order_id: uuid) -> int:
        order: OrderBookEntry = self.order_id_map.get(unique_order_id)
        if order is None:
            raise KeyError("No order was found with given id.")

        position_of_order = order.limit.position

        result: int = 0
        if position_of_order < self.highest_buy.position:
            pass
        elif position_of_order == self.highest_buy.position:
            result = order.total_amount_to_head()
        else:
            for index in range(self.highest_buy.position, position_of_order):
                result += self.buy_limits[index].size

            result += order.total_amount_to_head()

        return result
