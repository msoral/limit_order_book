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
    event_time: Optional[int] = field(default=None)
    next_order: Optional[OrderBookEntry] = field(default=None, repr=False)
    prev_order: Optional[OrderBookEntry] = field(default=None, repr=False)
    limit: 'Limit' = field(default=None, repr=False)  # To avoid circular import

    def add_to_head(self, other_order: OrderBookEntry) -> None:
        if other_order:
            self.next_order = other_order
            other_order.prev_order = self

    def add_to_tail(self, other_order: OrderBookEntry) -> None:
        if other_order:
            self.prev_order = other_order
            other_order.next_order = self

    def break_link(self):
        if self.prev_order:
            self.prev_order.next_order = self.next_order
        if self.next_order:
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
