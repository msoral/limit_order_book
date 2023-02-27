from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Optional


@dataclass(slots=True)
class OrderBookEntry:
    unique_id: uuid
    amount: int
    price: float
    is_buy: bool
    entry_time: int
    event_time: Optional[int] = field(init=False)
    next_order: Optional[OrderBookEntry] = field(init=False, repr=False)
    prev_order: Optional[OrderBookEntry] = field(init=False, repr=False)
    limit: 'Limit' = field(init=False, repr=False)  # To avoid circular import

    def add_to_head(self, other_order: OrderBookEntry) -> None:
        self.next_order = other_order
        other_order.prev_order = self

    def add_to_tail(self, other_order: OrderBookEntry) -> None:
        self.prev_order = other_order
        other_order.next_order = self

    def break_link(self):
        self.prev_order.next_order = self.next_order
        self.next_order.prev_order = self.prev_order
        self.prev_order = None
        self.next_order = None

    def total_amount_to_head(self) -> int:
        amount = 0
        order = self
        while order.prev_order:
            order = order.prev_order
            amount += order.amount
        return amount

    def __hash__(self) -> int:
        return self.unique_id.__hash__()
