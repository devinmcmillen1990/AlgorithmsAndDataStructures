from __future__ import annotations
from collections.abc import Iterable, Iterator
from reprlib import recursive_repr
from typing import Any


from data_structures.linked_lists.singly_linked.node import Node


class LinkedList:

    def __init__(self, values:Iterable[Any]=()) -> None:
        self._head: Node|None = None
        self._tail: Node|None = None
        self._size = 0
        for value in values:
            self.append(value=value)

    def prepend(self, value: Any) -> None:
        node = Node(value=value, next=self._head)
        self._head = node
        if self._tail is None:
            self._tail = node
        self._size += 1

    def append(self, value: Any) -> None:
        node = Node(value=value, next=None)
        if self._tail is None:
            self._head = node
        else:
            self._tail.next = node
        self._tail = node
        self._size += 1

    def insert(self, index: int, value: Any) -> None:
        index = self._normalize_index(index=index, for_insert=True)
        if index == 0:
            self.prepend(value=value)
        elif index == self._size:
            self.append(value=value)
        else:
            previous = self._node_at(index-1)
            previous.next = Node(value=value, next=previous.next)
            self._size += 1

    def extend(self, values: Iterable[Any]) -> None:
        if values is self:
            values = list(self)
        for value in values:
            self.append(value=value)

    def index(self, value: Any) -> int | None:
        node = self._head
        index = 0
        while node is not None:
            if node.value is value or node.value == value:
                return index
            index += 1
            node = node.next
        return None

    def count(self, value: Any) -> int:
        return sum(1 for item in self if item is value or item == value)

    def pop(self, index: int=-1) -> Any:
        index = self._normalize_index(index=index)
        if index == 0:
            node = self._head
            assert node is not None
            self._head = node.next
            if self._head is None:
                self._tail = None
        else:
            previous = self._node_at(index-1)
            node = previous.next
            assert node is not None
            previous.next = node.next
            if node is self._tail:
                self._tail = previous
        self._size -= 1
        node.next = None    # Detach from Linked List                       
        return node.value

    def remove(self, value: Any) -> None:
        index = self.index(value=value)
        if index is None:
            raise ValueError(f'{value!r} is not in the linked list')
        self.pop(index=index)

    def clear(self) -> None:
        while self._head is not None:
            self.pop(0)

    def reverse(self) -> LinkedList:
        reversed_list = LinkedList()
        for value in self:
            reversed_list.prepend(value=value)
        return reversed_list

    def _normalize_index(self, index: int, *, for_insert: bool = False) -> int:
        if not isinstance(index, int):
            raise TypeError("index must be an integer; slicing is not supported")
        if for_insert:
            if index < 0:
                index += self._size
            return max(0, min(index, self._size))               # Allow insertion at positions 0 through size, inclusive.
        if index < -self._size or index >= self._size:          # Reading/removing requires an existing element.
            raise IndexError("linked list index out of range")
        return index if index >= 0 else index + self._size

    def _node_at(self, index: int) -> Node:
        index = self._normalize_index(index=index)
        if index == (self._size-1): 
            return self._tail
        node = self._head
        while index > 0:
            assert node is not None
            node = node.next
            index -= 1
        assert node is not None
        return node

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[Any]:
        current = self._head
        while current is not None:
            yield current.value
            current = current.next
    
    def __contains__(self, value: Any) -> bool:
        return any(item is value or item == value for item in self)

    def __getitem__(self, index: int) -> Any:
        return self._node_at(index=index).value

    def __setitem__(self, index: int, value: Any) -> None:
        self._node_at(index=index).value = value

    def __delitem__(self, index) -> None:
        self.pop(index=index)

    @recursive_repr()
    def __repr__(self):
        return f"LinkedList({list(self)!r})"

