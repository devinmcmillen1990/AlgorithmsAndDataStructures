from __future__ import annotations
from collections.abc import Iterable, Iterator
from reprlib import recursive_repr
from typing import Any


from node import Node


class LinkedList:

    def __init__(self, values:Iterable[Any]=()) -> None:
        self._head: Node|Node=None
        self._tail: Node|Node=None
        self._size = 0
        for value in values:
            self.append(value=value)

    def prepend(self, value: Any) -> None:
        node = Node(value=value, next=self._head)
        self._head = node
        if self.tail is None:
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
        index = self._normalize_index(index=index)
        if index == 0:
            self.prepend(value=value)
        elif index == (self._size-1):
            self.append(value=value)
        else:
            previous = self._node_at(index-1)
            previous.next = Node(value=value, next=previous.next)
            self._size += 1

    def extend(self, values: Iterable[Any]) -> None:
        if values is None:
            return
        for value in values:
            self.append(value=value)

    def index(self, value: Any) -> int:
        if value is None: 
            return -1
        node = self._head
        index = 0
        while node is not None:
            if node.value == value:
                return index
            index += 1
            node = node.next
        return -1

    def count(self, value: Any) -> int:
        return sum(1 for item in self if item is value or item == value)

    def pop(self, index: int=0) -> Node:
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
        return node

    def remove(self, value: Any) -> None:
        index = self.index(value=value)
        self.pop(index=index)

    def clear(self) -> None:
        while self._head is not None:
            self.pop(0)

    def reverse(self) -> LinkedList:
        reversed_list = LinkedList()
        for value in self:
            reversed_list.prepend(value=value)
        return reversed_list

    def _normalize_index(self, index: int) -> int:
        if not isinstance(index, int): 
            raise TypeError("index must be an integer; slicing is not supported")
        if index < -(self._size) or index >= self._size: 
            raise IndexError("linked list index out of range")
        return index if index >= 0 else (index + self._size)

    def _node_at(self, index: int) -> Node:
        index = self._normalize_index(index=index)
        if index == (self._size-1): 
            return self._tail
        node = self._head
        while index > 0:
            assert node is not None
            node = node.next
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
        return self._node_at(index=index)

    def __setitem__(self, index: int, value: Any) -> None:
        self._node_at(index=index).value = value

    def __delitem__(self, index) -> None:
        self.pop(index=index)

    @recursive_repr()
    def __repr__(self):
        return f"LinkedList({list(self)!r})"

