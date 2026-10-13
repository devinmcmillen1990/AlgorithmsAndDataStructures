from __future__ import annotations

import sys
import unittest
from itertools import islice
from pathlib import Path
from unittest.mock import patch


PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from data_structures.linked_list.linkedlist import LinkedList
from data_structures.linked_list.node import Node


class TestLinkedList(unittest.TestCase):
    def assert_list(self, linked: LinkedList, expected: list) -> list[Node]:
        """Check the values AND the chain, length, head, and tail."""
        self.assertIsInstance(linked, LinkedList)
        nodes = []
        seen = set()
        current = linked._head

        # Check links first: a cycle should fail, not make this check loop.
        while current is not None:
            self.assertNotIn(id(current), seen, "Cycle detected in node links")
            self.assertLess(len(nodes), len(expected), "Too many linked nodes")
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
            self.assertIsNone(linked._tail.next)

        # Limit iteration in case a rewritten __iter__ repeatedly yields values.
        self.assertEqual(list(islice(linked, len(expected) + 1)), expected)
        return nodes

    def test_node(self) -> None:
        last = Node(20)
        first = Node(10, last)
        self.assertEqual(first.value, 10)
        self.assertIs(first.next, last)
        self.assertEqual(last.value, 20)
        self.assertIsNone(last.next)

    def test_constructor(self) -> None:
        self.assert_list(LinkedList(), [])
        for values in ([], [10], [10, 20, 30], [10, 10], [None, 0, False, ""]):
            with self.subTest(values=values):
                self.assert_list(LinkedList(values), values)

    def test_constructor_accepts_iterables(self) -> None:
        sources = (
            (10, 20, 30),
            (value for value in [10, 20, 30]),
            LinkedList([10, 20, 30]),
        )
        for source in sources:
            with self.subTest(source_type=type(source).__name__):
                self.assert_list(LinkedList(source), [10, 20, 30])

    def test_prepend(self) -> None:
        linked = LinkedList()
        for value, expected in ((20, [20]), (10, [10, 20]), (0, [0, 10, 20])):
            self.assertIsNone(linked.prepend(value))
            self.assert_list(linked, expected)

    def test_append(self) -> None:
        linked = LinkedList()
        for value, expected in ((10, [10]), (20, [10, 20]), (30, [10, 20, 30])):
            self.assertIsNone(linked.append(value))
            self.assert_list(linked, expected)

    def test_insert(self) -> None:
        for values in ([], [10], [10, 20, 30]):
            for index in range(-6, 7):
                with self.subTest(values=values, index=index):
                    linked = LinkedList(values)
                    expected = values.copy()
                    expected.insert(index, 99)
                    self.assertIsNone(linked.insert(index, 99))
                    self.assert_list(linked, expected)

    def test_extend(self) -> None:
        for initial in ([], [10]):
            for extra in ([], [20, 30]):
                with self.subTest(initial=initial, extra=extra):
                    linked = LinkedList(initial)
                    self.assertIsNone(linked.extend(extra))
                    self.assert_list(linked, initial + extra)

    def test_extend_accepts_iterables(self) -> None:
        sources = ((20, 30), (x for x in [20, 30]), LinkedList([20, 30]))
        for source in sources:
            with self.subTest(source_type=type(source).__name__):
                linked = LinkedList([10])
                self.assertIsNone(linked.extend(source))
                self.assert_list(linked, [10, 20, 30])

    def test_extend_self(self) -> None:
        for values in ([], [10, 20, 30]):
            with self.subTest(values=values):
                linked = LinkedList(values)
                original_append = linked.append
                calls = 0

                # Catch the common endless self-extension bug before it fills RAM.
                def guarded_append(value):
                    nonlocal calls
                    calls += 1
                    self.assertLessEqual(calls, len(values), "Endless self-extension")
                    return original_append(value)

                with patch.object(linked, "append", side_effect=guarded_append):
                    self.assertIsNone(linked.extend(linked))
                self.assert_list(linked, values + values)

    def test_pop_default(self) -> None:
        linked = LinkedList([10, 20, 30])
        for value, expected in ((30, [10, 20]), (20, [10]), (10, [])):
            self.assertEqual(linked.pop(), value)
            self.assert_list(linked, expected)
        with self.assertRaises(IndexError):
            linked.pop()
        self.assert_list(linked, [])

    def test_pop_indexed(self) -> None:
        for values in ([10], [10, 20, 30]):
            for index in range(-len(values), len(values)):
                with self.subTest(values=values, index=index):
                    linked = LinkedList(values)
                    expected = values.copy()
                    self.assertEqual(linked.pop(index), expected.pop(index))
                    self.assert_list(linked, expected)
                    linked.append(99)  # Also expose a stale tail after removal.
                    self.assert_list(linked, expected + [99])

    def test_remove(self) -> None:
        cases = (
            ([10], 10, []),
            ([10, 20, 30], 10, [20, 30]),
            ([10, 20, 30], 20, [10, 30]),
            ([10, 20, 30], 30, [10, 20]),
            ([10, 20, 20, 30], 20, [10, 20, 30]),
            ([None, 10], None, [10]),
        )
        for initial, value, expected in cases:
            with self.subTest(initial=initial, value=value):
                linked = LinkedList(initial)
                self.assertIsNone(linked.remove(value))
                self.assert_list(linked, expected)

    def test_missing_values(self) -> None:
        for values in ([], [10, 20]):
            with self.subTest(values=values):
                linked = LinkedList(values)
                self.assertIsNone(linked.index(99))
                self.assert_list(linked, values)
                with self.assertRaises(ValueError):
                    linked.remove(99)
                self.assert_list(linked, values)

    def test_clear(self) -> None:
        for values in ([], [10], [10, 20, 30]):
            with self.subTest(values=values):
                linked = LinkedList(values)
                for _ in range(2):  # Repeated clearing must also be safe.
                    self.assertIsNone(linked.clear())
                    self.assert_list(linked, [])

    def test_reuse_after_becoming_empty(self) -> None:
        actions = {
            "pop_last": lambda linked: linked.pop(),
            "pop_first": lambda linked: linked.pop(0),
            "remove": lambda linked: linked.remove(10),
            "clear": lambda linked: linked.clear(),
            "delete": lambda linked: linked.__delitem__(0),
        }
        for name, action in actions.items():
            with self.subTest(operation=name):
                linked = LinkedList([10])
                action(linked)
                self.assert_list(linked, [])
                linked.append(20)
                linked.prepend(5)
                linked.append(30)
                self.assert_list(linked, [5, 20, 30])

    def test_index(self) -> None:
        values = [10, 20, 20, 30, None]
        linked = LinkedList(values)
        for value, expected in ((10, 0), (20, 1), (30, 3), (None, 4)):
            with self.subTest(value=value):
                self.assertEqual(linked.index(value), expected)
                self.assert_list(linked, values)

    def test_count(self) -> None:
        values = [10, 20, 20, None]
        linked = LinkedList(values)
        for value, expected in ((10, 1), (20, 2), (None, 1), (99, 0)):
            with self.subTest(value=value):
                self.assertEqual(linked.count(value), expected)
                self.assert_list(linked, values)
        self.assertEqual(LinkedList().count(10), 0)

    def test_contains(self) -> None:
        linked = LinkedList([10, 20, None])
        self.assertIn(10, linked)
        self.assertIn(20, linked)
        self.assertIn(None, linked)
        self.assertNotIn(99, linked)
        self.assertNotIn(10, LinkedList())
        self.assert_list(linked, [10, 20, None])

    def test_searches_use_value_equality(self) -> None:
        stored = {"score": 10}
        equal_value = {"score": 10}  # Equal, but not the same object.
        linked = LinkedList([stored])
        self.assertIsNot(stored, equal_value)
        self.assertIn(equal_value, linked)
        self.assertEqual(linked.index(equal_value), 0)
        self.assertEqual(linked.count(equal_value), 1)
        self.assertIsNone(linked.remove(equal_value))
        self.assert_list(linked, [])

    def test_reverse(self) -> None:
        for values in ([], [10], [10, 20, 30], [10, 20, 10]):
            with self.subTest(values=values):
                original = LinkedList(values)
                before = self.assert_list(original, values)
                result = original.reverse()

                self.assertIsNot(result, original)
                result_nodes = self.assert_list(result, values[::-1])
                after = self.assert_list(original, values)
                self.assertEqual([id(n) for n in before], [id(n) for n in after])
                self.assertTrue(
                    {id(n) for n in before}.isdisjoint(id(n) for n in result_nodes),
                    "The original and reversed lists must not share nodes",
                )

    def test_reverse_structures_are_independent(self) -> None:
        original = LinkedList([10, 20, 30])
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
        original = LinkedList([first, second])
        result = original.reverse()
        self.assertIs(result[0], second)
        self.assertIs(result[1], first)
        result[0]["score"] = 99  # Mutate the shared value, not a node.
        self.assert_list(original, [{"score": 10}, {"score": 99}])
        self.assert_list(result, [{"score": 99}, {"score": 10}])

    def test_len_and_truthiness(self) -> None:
        linked = LinkedList()
        self.assertEqual(len(linked), 0)
        self.assertFalse(linked)
        linked.append(0)  # A false-valued element still makes the list nonempty.
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
                linked = LinkedList(values)
                for _ in range(2):  # Each new iterator starts at the head.
                    iterator = iter(linked)
                    for value in values:
                        self.assertEqual(next(iterator), value)
                    with self.assertRaises(StopIteration):
                        next(iterator)
                    with self.assertRaises(StopIteration):
                        next(iterator)
                self.assert_list(linked, values)

    def test_iterators_are_independent(self) -> None:
        linked = LinkedList([10, 20, 30])
        first, second = iter(linked), iter(linked)
        self.assertEqual(next(first), 10)
        self.assertEqual(next(first), 20)
        self.assertEqual(next(second), 10)
        self.assertEqual(list(islice(first, 2)), [30])
        self.assertEqual(list(islice(second, 3)), [20, 30])
        self.assert_list(linked, [10, 20, 30])

    def test_getitem(self) -> None:
        values = [10, 20, 30]
        linked = LinkedList(values)
        for index in range(-3, 3):
            with self.subTest(index=index):
                self.assertEqual(linked[index], values[index])
                self.assert_list(linked, values)

    def test_setitem(self) -> None:
        for index in range(-3, 3):
            with self.subTest(index=index):
                linked = LinkedList([10, 20, 30])
                expected = [10, 20, 30]
                expected[index] = 99
                linked[index] = 99
                self.assert_list(linked, expected)

    def test_delitem(self) -> None:
        for values in ([10], [10, 20, 30]):
            for index in range(-len(values), len(values)):
                with self.subTest(values=values, index=index):
                    linked = LinkedList(values)
                    expected = values.copy()
                    del expected[index]
                    del linked[index]
                    self.assert_list(linked, expected)

    def test_repr(self) -> None:
        for values in ([], [10], [10, 20, 30], ["hello", None]):
            with self.subTest(values=values):
                linked = LinkedList(values)
                self.assert_list(linked, values)
                self.assertEqual(repr(linked), f"LinkedList({values!r})")

    def test_repr_handles_self_reference(self) -> None:
        linked = LinkedList()
        linked.append(linked)
        self.assertEqual(repr(linked), "LinkedList([...])")

    def test_normalize_index(self) -> None:
        linked = LinkedList([10, 20, 30])
        cases = ((-3, 0), (-2, 1), (-1, 2), (0, 0), (1, 1), (2, 2))
        for index, expected in cases:
            with self.subTest(index=index):
                self.assertEqual(linked._normalize_index(index), expected)
        self.assert_list(linked, [10, 20, 30])

    def test_normalize_index_for_insert(self) -> None:
        linked = LinkedList([10, 20, 30])
        cases = ((-10, 0), (-3, 0), (-2, 1), (-1, 2), (0, 0), (2, 2), (3, 3), (10, 3))
        for index, expected in cases:
            with self.subTest(index=index):
                self.assertEqual(linked._normalize_index(index, for_insert=True), expected)
        empty = LinkedList()
        for index in (-10, -1, 0, 1, 10):
            with self.subTest(empty_index=index):
                self.assertEqual(empty._normalize_index(index, for_insert=True), 0)
        self.assert_list(linked, [10, 20, 30])
        self.assert_list(empty, [])

    def test_node_at(self) -> None:
        linked = LinkedList([10, 20, 30])
        nodes = self.assert_list(linked, [10, 20, 30])
        for index in range(-3, 3):
            with self.subTest(index=index):
                self.assertIs(linked._node_at(index), nodes[index])
        self.assert_list(linked, [10, 20, 30])

    def test_invalid_indices(self) -> None:
        actions = {
            "getitem": lambda linked, i: linked[i],
            "setitem": lambda linked, i: linked.__setitem__(i, 99),
            "delitem": lambda linked, i: linked.__delitem__(i),
            "pop": lambda linked, i: linked.pop(i),
            "normalize": lambda linked, i: linked._normalize_index(i),
            "node_at": lambda linked, i: linked._node_at(i),
        }
        invalid_types = (None, "1", 1.5, slice(None))
        for values in ([], [10, 20, 30]):
            invalid_bounds = (-len(values) - 1, len(values), -99, 99)
            for error, indices in ((IndexError, invalid_bounds), (TypeError, invalid_types)):
                for index in indices:
                    for name, action in actions.items():
                        with self.subTest(values=values, index=index, operation=name):
                            linked = LinkedList(values)
                            with self.assertRaises(error):
                                action(linked, index)
                            self.assert_list(linked, values)

    def test_insert_rejects_invalid_types(self) -> None:
        for values in ([], [10, 20, 30]):
            for index in (None, "1", 1.5, slice(None)):
                with self.subTest(values=values, index=index):
                    linked = LinkedList(values)
                    with self.assertRaises(TypeError):
                        linked.insert(index, 99)
                    self.assert_list(linked, values)
                    with self.assertRaises(TypeError):
                        linked._normalize_index(index, for_insert=True)
                    self.assert_list(linked, values)


if __name__ == "__main__":
    unittest.main(verbosity=2)