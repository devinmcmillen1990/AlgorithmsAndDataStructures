from __future__ import annotations

from typing import Any


class Node:
    def __init__(self, value: Any, next: Node|Node=None) -> Node:
        self.value = value
        self.next = next
