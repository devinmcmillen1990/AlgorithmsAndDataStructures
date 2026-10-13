from __future__ import annotations

from typing import Any


class SinglyLinkedNode:
    def __init__(self, value: Any, next: SinglyLinkedNode|SinglyLinkedNode=None) -> SinglyLinkedNode:
        self.value = value
        self.next = next
