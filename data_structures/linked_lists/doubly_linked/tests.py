from __future__ import annotations

import sys
import unittest
from itertools import islice
from pathlib import Path
from unittest.mock import patch

PROJECT_ROOT = Path(__file__).resolve().parents[3]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from data_structures.linked_lists.doubly_linked.linkedlist import DoublyLinkedList
from data_structures.linked_lists.doubly_linked.node import Node


class TestDoublyLinkedList(unittest.TestCase):
    def assert_list(self, linked: DoublyLinkedList, expected: list) -> list[Node]:
        """Check values, endpoints, length, and links; return the actual nodes."""
        self.assertIsInstance(linked, DoublyLinkedList)
        nodes, seen = [], set()
        current = linked._head

        while current is not None:
            self.assertNotIn(id(current), seen, "Cycle in next links")
            self.assertLess(len(nodes), len(expected), "Too many nodes")
            self.assertIsInstance(current, Node)
            self.assertIs(current.prev, nodes[-1] if nodes else None,
                          "Incorrect prev link")
            seen.add(id(current))
            nodes.append(current)
            current = current.next

        self.assertEqual([node.value for node in nodes], expected)
        self.assertEqual(linked._size, len(expected))
        self.assertEqual(len(linked), len(expected))
        self.assertEqual(bool(linked), bool(expected))
        self.assertIs(linked._head, nodes[0] if nodes else None)
        self.assertIs(linked._tail, nodes[-1] if nodes else None)
        if nodes:
            self.assertIsNone(nodes[-1].next)
        self.assertEqual(list(islice(linked, len(expected) + 1)), expected)
        current = linked._tail
        for node in reversed(nodes):
            self.assertIs(current, node, "Backward chain disagrees with forward links")
            current = current.prev
        self.assertIsNone(current)
        return nodes

    def test_node_constructor(self) -> None:
        last = Node(30)
        first = Node(10, last)
        self.assertEqual(first.value, 10)
        self.assertIs(first.next, last)
        self.assertEqual(last.value, 30)
        self.assertIsNone(last.next)
        self.assertIsNone(last.prev)
        self.assertIsNone(first.prev)
        middle = Node(20, next=last, prev=first)
        self.assertEqual(middle.value, 20)
        self.assertIs(middle.next, last)
        self.assertIs(middle.prev, first)
        payload = {"score": 10}
        self.assertIs(Node(payload).value, payload)

    def test_constructor(self) -> None:
        self.assert_list(DoublyLinkedList(), [])
        for values in ([], [10], [10, 20, 30], [10, 10], [None, 0, False, ""]):
            with self.subTest(values=values):
                self.assert_list(DoublyLinkedList(values), values)

    def test_constructor_accepts_iterables(self) -> None:
        for source in ((10, 20), (x for x in (10, 20)), DoublyLinkedList([10, 20])):
            with self.subTest(source_type=type(source).__name__):
                self.assert_list(DoublyLinkedList(source), [10, 20])
        self.assert_list(DoublyLinkedList("ab"), ["a", "b"])
        for source in (None, 10):
            with self.subTest(source=source):
                with self.assertRaises(TypeError):
                    DoublyLinkedList(source)

    def test_constructor_creates_independent_nodes(self) -> None:
        payload = {"score": 10}
        original = DoublyLinkedList([payload, 20])
        copy = DoublyLinkedList(original)
        before = self.assert_list(original, [payload, 20])
        copied = self.assert_list(copy, [payload, 20])
        self.assertTrue({id(n) for n in before}.isdisjoint(id(n) for n in copied))
        self.assertIs(copy[0], payload)
        copy.append(30)
        self.assert_list(original, [payload, 20])
        self.assert_list(copy, [payload, 20, 30])

    def test_prepend(self) -> None:
        linked = DoublyLinkedList()
        for value, expected in ((20, [20]), (10, [10, 20]), (0, [0, 10, 20])):
            self.assertIsNone(linked.prepend(value))
            self.assert_list(linked, expected)

    def test_append(self) -> None:
        linked = DoublyLinkedList()
        for value, expected in ((10, [10]), (20, [10, 20]), (30, [10, 20, 30])):
            self.assertIsNone(linked.append(value))
            self.assert_list(linked, expected)

    def test_insert(self) -> None:
        for values in ([], [10], [10, 20, 30]):
            for index in (-99, *range(-6, 7), 99):
                with self.subTest(values=values, index=index):
                    linked = DoublyLinkedList(values)
                    expected = values.copy()
                    expected.insert(index, 99)
                    self.assertIsNone(linked.insert(index, 99))
                    self.assert_list(linked, expected)

    def test_extend(self) -> None:
        for initial in ([], [10]):
            for extra in ([], [20, 30], [None]):
                with self.subTest(initial=initial, extra=extra):
                    linked = DoublyLinkedList(initial)
                    self.assertIsNone(linked.extend(extra))
                    self.assert_list(linked, initial + extra)

    def test_extend_accepts_iterables(self) -> None:
        for source in ((20, 30), (x for x in (20, 30)), DoublyLinkedList([20, 30])):
            with self.subTest(source_type=type(source).__name__):
                linked = DoublyLinkedList([10])
                self.assertIsNone(linked.extend(source))
                self.assert_list(linked, [10, 20, 30])
        linked = DoublyLinkedList()
        linked.extend("ab")
        self.assert_list(linked, ["a", "b"])

    def test_extend_self(self) -> None:
        for values in ([], [10], [10, 20, 30]):
            with self.subTest(values=values):
                linked = DoublyLinkedList(values)
                before = self.assert_list(linked, values)
                append = linked.append
                calls = 0
                def guarded_append(value):
                    nonlocal calls
                    calls += 1
                    self.assertLessEqual(calls, len(values), "Endless self-extension")
                    return append(value)
                with patch.object(linked, "append", side_effect=guarded_append):
                    self.assertIsNone(linked.extend(linked))
                after = self.assert_list(linked, values + values)
                self.assertEqual(after[:len(values)], before)
                self.assertTrue({id(n) for n in before}.isdisjoint(
                    id(n) for n in after[len(values):]))

    def test_extend_rejects_non_iterables(self) -> None:
        for source in (None, 10):
            with self.subTest(source=source):
                linked = DoublyLinkedList([10])
                with self.assertRaises(TypeError):
                    linked.extend(source)
                self.assert_list(linked, [10])

    def test_extend_keeps_values_yielded_before_iterator_failure(self) -> None:
        def failing_source():
            yield 20
            raise RuntimeError("source failed")

        linked = DoublyLinkedList([10])
        with self.assertRaisesRegex(RuntimeError, "source failed"):
            linked.extend(failing_source())
        self.assert_list(linked, [10, 20])

    def test_pop_default(self) -> None:
        linked = DoublyLinkedList([10, 20, 30])
        for value, expected in ((30, [10, 20]), (20, [10]), (10, [])):
            self.assertEqual(linked.pop(), value)
            self.assert_list(linked, expected)
        with self.assertRaises(IndexError):
            linked.pop()
        self.assert_list(linked, [])

    def test_pop_indexed_and_detaches_node(self) -> None:
        for values in ([10], [10, 20, 30], list(range(8))):
            for index in range(-len(values), len(values)):
                with self.subTest(values=values, index=index):
                    linked = DoublyLinkedList(values)
                    expected = values.copy()
                    nodes = self.assert_list(linked, expected)
                    removed = nodes[index]
                    self.assertEqual(linked.pop(index), expected.pop(index))
                    self.assertIsNone(removed.next)
                    self.assertIsNone(removed.prev)
                    self.assert_list(linked, expected)
                    linked.append(99)
                    self.assert_list(linked, expected + [99])

    def test_pop_returns_original_value_not_node(self) -> None:
        payload = {"score": 10}
        linked = DoublyLinkedList([payload])
        self.assertIs(linked.pop(), payload)
        self.assert_list(linked, [])

    def test_remove(self) -> None:
        cases = (
            ([10], 10, []),
            ([10, 20, 30], 10, [20, 30]),
            ([10, 20, 30], 20, [10, 30]),
            ([10, 20, 30], 30, [10, 20]),
            ([10, 20, 20, 30], 20, [10, 20, 30]),
            ([None, 10], None, [10]),
            ([0, 10], 0, [10]),
        )
        for initial, value, expected in cases:
            with self.subTest(initial=initial, value=value):
                linked = DoublyLinkedList(initial)
                self.assertIsNone(linked.remove(value))
                self.assert_list(linked, expected)

    def test_remove_missing_raises_without_mutation(self) -> None:
        for values in ([], [10], [10, 20]):
            with self.subTest(values=values):
                linked = DoublyLinkedList(values)
                before = self.assert_list(linked, values)
                with self.assertRaises(ValueError):
                    linked.remove(99)
                self.assertEqual(self.assert_list(linked, values), before)

    def test_clear_detaches_nodes_and_is_repeatable(self) -> None:
        for values in ([], [10], [10, 20, 30]):
            with self.subTest(values=values):
                linked = DoublyLinkedList(values)
                nodes = self.assert_list(linked, values)
                self.assertIsNone(linked.clear())
                self.assert_list(linked, [])
                for node in nodes:
                    self.assertIsNone(node.next)
                    self.assertIsNone(node.prev)
                self.assertIsNone(linked.clear())
                linked.append(99)
                self.assert_list(linked, [99])

    def test_reuse_after_becoming_empty(self) -> None:
        for operation in ("pop", "remove", "delete", "clear"):
            with self.subTest(operation=operation):
                linked = DoublyLinkedList([10])
                if operation == "pop":
                    linked.pop(0)
                elif operation == "remove":
                    linked.remove(10)
                elif operation == "delete":
                    del linked[0]
                else:
                    linked.clear()
                self.assert_list(linked, [])
                linked.prepend(20)
                linked.append(30)
                self.assert_list(linked, [20, 30])

    def test_index(self) -> None:
        values = [10, 20, 20, 30, None, 0]
        linked = DoublyLinkedList(values)
        for value, expected in ((10, 0), (20, 1), (30, 3), (None, 4), (0, 5)):
            with self.subTest(value=value):
                position = linked.index(value)
                self.assertIs(type(position), int)
                self.assertEqual(position, expected)
                self.assert_list(linked, values)

    def test_index_missing_returns_none(self) -> None:
        for values in ([], [10], [10, 20]):
            with self.subTest(values=values):
                linked = DoublyLinkedList(values)
                self.assertIsNone(linked.index(99))
                self.assertIsNone(linked.index(None))
                self.assert_list(linked, values)

    def test_count(self) -> None:
        values = [10, 20, 20, None]
        linked = DoublyLinkedList(values)
        for value, expected in ((10, 1), (20, 2), (None, 1), (99, 0)):
            with self.subTest(value=value):
                count = linked.count(value)
                self.assertIs(type(count), int)
                self.assertEqual(count, expected)
        self.assertEqual(DoublyLinkedList().count(10), 0)
        self.assert_list(linked, values)

    def test_contains(self) -> None:
        linked = DoublyLinkedList([10, 20, None])
        self.assertIn(10, linked)
        self.assertIn(20, linked)
        self.assertIn(None, linked)
        self.assertNotIn(99, linked)
        self.assertNotIn(10, DoublyLinkedList())
        self.assert_list(linked, [10, 20, None])

    def test_searches_use_identity_or_equality(self) -> None:
        stored, query = {"score": 10}, {"score": 10}
        self.assertIsNot(stored, query)
        linked = DoublyLinkedList([stored])
        self.assertIn(query, linked)
        self.assertEqual(linked.index(query), 0)
        self.assertEqual(linked.count(query), 1)
        self.assertIsNone(linked.remove(query))
        self.assert_list(linked, [])
        value = float("nan")
        linked = DoublyLinkedList([value, value])
        self.assertIn(value, linked)
        self.assertEqual(linked.index(value), 0)
        self.assertEqual(linked.count(value), 2)
        self.assertIsNone(linked.index(float("nan")))
        linked.remove(value)
        self.assert_list(linked, [value])

    def test_reverse(self) -> None:
        for values in ([], [10], [10, 20, 30], [10, 20, 10]):
            with self.subTest(values=values):
                original = DoublyLinkedList(values)
                before = self.assert_list(original, values)
                result = original.reverse()
                self.assertIsNot(result, original)
                copied = self.assert_list(result, values[::-1])
                self.assertEqual(self.assert_list(original, values), before)
                self.assertTrue({id(n) for n in before}.isdisjoint(id(n) for n in copied))

    def test_reverse_structures_are_independent(self) -> None:
        original = DoublyLinkedList([10, 20, 30])
        result = original.reverse()
        result[0] = 99
        result.append(40)
        self.assert_list(result, [99, 20, 10, 40])
        self.assert_list(original, [10, 20, 30])
        original.prepend(5)
        self.assert_list(original, [5, 10, 20, 30])
        self.assert_list(result, [99, 20, 10, 40])

    def test_reverse_is_shallow_copy(self) -> None:
        first, second = {"score": 10}, {"score": 20}
        original = DoublyLinkedList([first, second])
        result = original.reverse()
        self.assertIs(result[0], second)
        self.assertIs(result[1], first)
        result[0]["score"] = 99
        self.assert_list(original, [{"score": 10}, {"score": 99}])
        self.assert_list(result, [{"score": 99}, {"score": 10}])

    def test_len_and_truthiness(self) -> None:
        linked = DoublyLinkedList()
        self.assertEqual(len(linked), 0)
        self.assertFalse(linked)
        linked.append(0)
        self.assertEqual(len(linked), 1)
        self.assertTrue(linked)
        linked.prepend(10)
        self.assertEqual(len(linked), 2)
        linked.clear()
        self.assertEqual(len(linked), 0)
        self.assertFalse(linked)

    def test_iteration(self) -> None:
        for values in ([], [10], [10, 20, 30]):
            with self.subTest(values=values):
                linked = DoublyLinkedList(values)
                iterator = iter(linked)
                self.assertIs(iter(iterator), iterator)
                for value in values:
                    self.assertEqual(next(iterator), value)
                for _ in range(2):
                    with self.assertRaises(StopIteration):
                        next(iterator)
                self.assert_list(linked, values)

    def test_iterators_are_independent(self) -> None:
        linked = DoublyLinkedList([10, 20, 30])
        first, second = iter(linked), iter(linked)
        self.assertEqual(next(first), 10)
        self.assertEqual(next(first), 20)
        self.assertEqual(next(second), 10)
        self.assertEqual(list(islice(first, 2)), [30])
        self.assertEqual(list(islice(second, 3)), [20, 30])
        self.assert_list(linked, [10, 20, 30])

    def test_getitem(self) -> None:
        for values in ([10], [10, 20, 30], list(range(8))):
            linked = DoublyLinkedList(values)
            for index in range(-len(values), len(values)):
                with self.subTest(values=values, index=index):
                    self.assertEqual(linked[index], values[index])
            self.assert_list(linked, values)

    def test_setitem_preserves_nodes(self) -> None:
        for index in range(-3, 3):
            with self.subTest(index=index):
                linked = DoublyLinkedList([10, 20, 30])
                before = self.assert_list(linked, [10, 20, 30])
                expected = [10, 20, 30]
                expected[index] = 99
                linked[index] = 99
                self.assertEqual(self.assert_list(linked, expected), before)
                self.assertIsNone(linked.__setitem__(index, 99))
                self.assertEqual(self.assert_list(linked, expected), before)

    def test_delitem(self) -> None:
        for values in ([10], [10, 20, 30]):
            for index in range(-len(values), len(values)):
                with self.subTest(values=values, index=index):
                    linked = DoublyLinkedList(values)
                    expected = values.copy()
                    del expected[index]
                    del linked[index]
                    self.assert_list(linked, expected)
        linked = DoublyLinkedList([10])
        self.assertIsNone(linked.__delitem__(0))
        self.assert_list(linked, [])

    def test_repr(self) -> None:
        for values in ([], [10], [10, 20, 30], ["hello", None]):
            with self.subTest(values=values):
                linked = DoublyLinkedList(values)
                self.assertEqual(repr(linked), f"DoublyLinkedList({values!r})")
                self.assert_list(linked, values)

    def test_repr_handles_self_reference(self) -> None:
        linked = DoublyLinkedList()
        linked.append(linked)
        self.assertEqual(repr(linked), "DoublyLinkedList([...])")
        linked.clear()

    def test_normalize_index(self) -> None:
        linked = DoublyLinkedList([10, 20, 30])
        cases = ((-3, 0), (-2, 1), (-1, 2), (0, 0), (1, 1), (2, 2))
        for index, expected in cases:
            with self.subTest(index=index):
                self.assertEqual(linked._normalize_index(index), expected)
        self.assert_list(linked, [10, 20, 30])

    def test_normalize_index_for_insert(self) -> None:
        linked = DoublyLinkedList([10, 20, 30])
        cases = ((-99, 0), (-3, 0), (-2, 1), (-1, 2), (0, 0), (2, 2), (3, 3), (99, 3))
        for index, expected in cases:
            with self.subTest(index=index):
                self.assertEqual(linked._normalize_index(index, for_insert=True), expected)
        empty = DoublyLinkedList()
        for index in (-99, -1, 0, 1, 99):
            with self.subTest(empty_index=index):
                self.assertEqual(empty._normalize_index(index, for_insert=True), 0)
        self.assert_list(linked, [10, 20, 30])
        self.assert_list(empty, [])

    def test_node_at(self) -> None:
        for values in ([10], [10, 20], [10, 20, 30], list(range(8))):
            linked = DoublyLinkedList(values)
            nodes = self.assert_list(linked, values)
            for index in range(-len(values), len(values)):
                with self.subTest(values=values, index=index):
                    self.assertIs(linked._node_at(index), nodes[index])
            self.assert_list(linked, values)

    def test_invalid_indices(self) -> None:
        for values in ([], [10], [10, 20, 30]):
            for index in (-len(values) - 1, len(values), -99, 99):
                with self.subTest(values=values, index=index):
                    linked = DoublyLinkedList(values)
                    with self.assertRaises(IndexError):
                        linked[index]
                    with self.assertRaises(IndexError):
                        linked[index] = 99
                    with self.assertRaises(IndexError):
                        del linked[index]
                    with self.assertRaises(IndexError):
                        linked.pop(index)
                    with self.assertRaises(IndexError):
                        linked._normalize_index(index)
                    with self.assertRaises(IndexError):
                        linked._node_at(index)
                    self.assert_list(linked, values)

    def test_invalid_index_types_and_slices(self) -> None:
        for values in ([], [10, 20, 30]):
            for index in (None, "1", 1.5, [], {}, slice(None), slice(0, 2)):
                with self.subTest(values=values, index=index):
                    linked = DoublyLinkedList(values)
                    with self.assertRaises(TypeError):
                        linked[index]
                    with self.assertRaises(TypeError):
                        linked[index] = 99
                    with self.assertRaises(TypeError):
                        del linked[index]
                    with self.assertRaises(TypeError):
                        linked.pop(index)
                    with self.assertRaises(TypeError):
                        linked.insert(index, 99)
                    with self.assertRaises(TypeError):
                        linked._normalize_index(index)
                    with self.assertRaises(TypeError):
                        linked._normalize_index(index, for_insert=True)
                    with self.assertRaises(TypeError):
                        linked._node_at(index)
                    self.assert_list(linked, values)

    def test_boolean_indices(self) -> None:
        linked = DoublyLinkedList([10, 20])
        self.assertEqual(linked[False], 10)
        self.assertEqual(linked[True], 20)
        linked[True] = 30
        self.assert_list(linked, [10, 30])
        linked.insert(True, 20)
        self.assert_list(linked, [10, 20, 30])
        self.assertEqual(linked.pop(False), 10)
        self.assert_list(linked, [20, 30])
        del linked[True]
        self.assert_list(linked, [20])

    def test_mixed_operations(self) -> None:
        linked = DoublyLinkedList()
        linked.append(20)
        self.assert_list(linked, [20])
        linked.prepend(10)
        self.assert_list(linked, [10, 20])
        linked.insert(1, 15)
        self.assert_list(linked, [10, 15, 20])
        linked.extend([30, 40])
        self.assert_list(linked, [10, 15, 20, 30, 40])
        self.assertEqual(linked.pop(-2), 30)
        self.assert_list(linked, [10, 15, 20, 40])
        linked.remove(15)
        self.assert_list(linked, [10, 20, 40])
        linked[-1] = 50
        self.assert_list(linked, [10, 20, 50])
        del linked[0]
        self.assert_list(linked, [20, 50])
        self.assert_list(linked.reverse(), [50, 20])
        self.assert_list(linked, [20, 50])
        linked.clear()
        self.assert_list(linked, [])

    def test_reversed_iteration(self) -> None:
        for values in ([], [10], [10, 20, 30]):
            with self.subTest(values=values):
                linked = DoublyLinkedList(values)
                before = self.assert_list(linked, values)
                iterator = reversed(linked)
                self.assertIs(iter(iterator), iterator)
                for value in values[::-1]:
                    self.assertEqual(next(iterator), value)
                for _ in range(2):
                    with self.assertRaises(StopIteration):
                        next(iterator)
                self.assertEqual(self.assert_list(linked, values), before)

    def test_reversed_iterators_are_independent(self) -> None:
        linked = DoublyLinkedList([10, 20, 30])
        first, second = reversed(linked), reversed(linked)
        self.assertEqual(next(first), 30)
        self.assertEqual(next(first), 20)
        self.assertEqual(next(second), 30)
        self.assertEqual(list(islice(first, 2)), [10])
        self.assertEqual(list(islice(second, 3)), [20, 10])
        self.assert_list(linked, [10, 20, 30])

    def test_reversed_uses_prev_links_not_indexed_access(self) -> None:
        linked = DoublyLinkedList([10, 20, 30])
        with patch.object(linked, "_node_at", side_effect=AssertionError("Indexed traversal")):
            self.assertEqual(list(islice(reversed(linked), 4)), [30, 20, 10])
        self.assert_list(linked, [10, 20, 30])

    def test_insert_and_pop_repair_both_neighbor_links(self) -> None:
        linked = DoublyLinkedList([10, 30])
        first, last = self.assert_list(linked, [10, 30])
        linked.insert(1, 20)
        middle = first.next
        self.assertIsNotNone(middle)
        self.assertIs(middle.prev, first)
        self.assertIs(middle.next, last)
        self.assertIs(last.prev, middle)
        self.assert_list(linked, [10, 20, 30])

        self.assertEqual(linked.pop(1), 20)
        self.assertIs(first.next, last)
        self.assertIs(last.prev, first)
        self.assertIsNone(middle.next)
        self.assertIsNone(middle.prev)
        self.assert_list(linked, [10, 30])

    def test_node_at_chooses_nearer_end(self) -> None:
        class ProbeNode:
            def __init__(self, value):
                self.value = value
                self.forward = self.backward = None
                self.next_reads = self.prev_reads = 0

            @property
            def next(self):
                self.next_reads += 1
                return self.forward

            @property
            def prev(self):
                self.prev_reads += 1
                return self.backward

        nodes = [ProbeNode(i) for i in range(8)]
        for index, node in enumerate(nodes):
            node.forward = nodes[index + 1] if index + 1 < len(nodes) else None
            node.backward = nodes[index - 1] if index else None
        linked = DoublyLinkedList()
        linked._head, linked._tail, linked._size = nodes[0], nodes[-1], len(nodes)

        for index, next_reads, prev_reads in ((0, 0, 0), (1, 1, 0), (6, 0, 1), (7, 0, 0)):
            with self.subTest(index=index):
                for node in nodes:
                    node.next_reads = node.prev_reads = 0
                self.assertIs(linked._node_at(index), nodes[index])
                self.assertEqual(sum(n.next_reads for n in nodes), next_reads)
                self.assertEqual(sum(n.prev_reads for n in nodes), prev_reads)


if __name__ == "__main__":
    unittest.main(verbosity=2)