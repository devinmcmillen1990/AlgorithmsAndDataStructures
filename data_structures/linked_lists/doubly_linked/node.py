from __future__ import annotations

from typing import Any


class DoublyLinkedNode:
    def __init__(self, value: Any, next: DoublyLinkedNode|None=None, prev: DoublyLinkedNode|None=None) -> None:
        self.value = value
        self.next = next
        self.prev = prev
