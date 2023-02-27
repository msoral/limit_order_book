from typing import TypeVar

T = TypeVar("T")


class Node:
    def __init__(self, data: T):
        self.data: T = data
        self.next = None
        self.prev = None
