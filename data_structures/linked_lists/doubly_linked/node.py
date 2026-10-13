from __future__ import annotations

from typing import Any


class Node:
    def __init__(self, value: Any, next: Node|None=None, prev: Node|None=None) -> None:
        self.value = value
        self.next = next
        self.prev = prev
