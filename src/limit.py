from dataclasses import dataclass, field

from src.orderbookentry import OrderBookEntry


@dataclass(slots=True)
class Limit:
    price: float = field(compare=True)
    position: int
    size: int = field(default=0, compare=False)
    total_volume: int = field(default=0, compare=False)  # Increases with execute only.
    head_order: 'OrderBookEntry' = field(init=False, repr=False, compare=False)
    tail_order: 'OrderBookEntry' = field(init=False, repr=False, compare=False)

    def __hash__(self) -> int:
        return self.price.__hash__()

    def add(self, order: OrderBookEntry) -> 'Limit':
        order.add_to_tail(self.tail_order)

        self.tail_order = order
        self.size += order.amount
        return self

    def remove(self, order: OrderBookEntry) -> None:
        order.break_link()
        self.size -= order.amount
        self._update_pointers(order)

    def execute(self, order: OrderBookEntry) -> None:
        order.break_link()
        self.size -= order.amount
        self.total_volume += order.amount
        self._update_pointers(order)

    def _update_pointers(self, order):
        if order == self.head_order:
            self.head_order = order.next_order

        if order == self.tail_order:
            self.tail_order = order.prev_order
