from __future__ import annotations

import sys
import random
import unittest
from copy import deepcopy
from itertools import islice
from pathlib import Path
from unittest.mock import patch


PROBLEM_DIR = Path(__file__).resolve().parent
# Expected location: <repository>/data_structures/linked_list/tests.py
PROJECT_ROOT = PROBLEM_DIR.parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from utils.load_test_cases import load_test_cases

from data_structures.linked_lists.singly_linked.node import SinglyLinkedNode
from data_structures.linked_lists.singly_linked.linkedlist import SinglyLinkedList
from data_structures.linked_lists.doubly_linked.node import DoublyLinkedNode
from data_structures.linked_lists.doubly_linked.linkedlist import DoublyLinkedList


CASE_PATH = Path(__file__).resolve().with_name('test_cases.json')
ERRORS = {'IndexError': IndexError, 'TypeError': TypeError, 'ValueError': ValueError}
ARITIES = {
    'prepend': {1}, 'append': {1}, 'insert': {2}, 'extend': {1},
    'pop': {0, 1}, 'remove': {1}, 'clear': {0}, 'index': {1},
    'count': {1}, 'reverse': {0}, 'getitem': {1}, 'setitem': {2},
    'delitem': {1}, 'contains': {1}, 'len': {0}, 'bool': {0}, 'iter': {0},
}
def validate_cases(cases: list[dict]) -> None:
    """Validate linked-list snapshot structure; file loading stays in utils."""
    if not isinstance(cases, list) or not cases:
        raise ValueError('test_cases.json must be a nonempty JSON array.')
    names = set()
    for case in cases:
        if not isinstance(case, dict) or set(case) != {'name', 'input', 'steps'}:
            raise ValueError('Each case needs exactly name, input, and steps.')
        name = case['name']
        if not isinstance(name, str) or not name or name in names:
            raise ValueError('Case names must be nonempty, unique strings.')
        names.add(name)
        if not isinstance(case['input'], list) or not isinstance(case['steps'], list):
            raise ValueError(f'{name}: input and steps must be arrays.')
        for number, step in enumerate(case['steps']):
            prefix = f'{name}, step {number}'
            if not isinstance(step, dict):
                raise ValueError(f'{prefix}: a step must be an object.')
            required = {'op', 'args', 'expected'}
            outcomes = set(step) - required
            if not required <= step.keys() or outcomes not in ({'expected_return'}, {'raises'}):
                raise ValueError(f'{prefix}: supply expected plus expected_return OR raises.')
            if not isinstance(step['op'], str) or step['op'] not in ARITIES:
                raise ValueError(f'{prefix}: unsupported operation.')
            if not isinstance(step['args'], list) or len(step['args']) not in ARITIES[step['op']]:
                raise ValueError(f'{prefix}: wrong argument count.')
            if not isinstance(step['expected'], list):
                raise ValueError(f'{prefix}: expected must be a list snapshot.')
            if 'raises' in step and (not isinstance(step['raises'], str) or step['raises'] not in ERRORS):
                raise ValueError(f'{prefix}: unsupported exception.')


class TestSinglyLinkedList(unittest.TestCase):
    """Shared contract tests; the doubly test class below reruns all of these."""
    List: type[SinglyLinkedList] | type[DoublyLinkedList] = SinglyLinkedList
    NodeType: type[SinglyLinkedNode] | type[DoublyLinkedNode] = SinglyLinkedNode
    DOUBLY = False

    @classmethod
    def setUpClass(cls) -> None:
        # Load once per implementation class using the shared repository helper.
        cls.cases = load_test_cases(PROBLEM_DIR / 'test_cases.json')
        validate_cases(cls.cases)

    def assert_list(self, linked, expected: list) -> list:
        """Verify values and node identity/link invariants, bounding traversals."""
        self.assertIsInstance(linked, self.List)
        nodes, seen = [], set()
        current = linked._head
        while current is not None:
            self.assertNotIn(id(current), seen, 'Cycle in next links')
            self.assertLess(len(nodes), len(expected), 'Too many nodes')
            self.assertIsInstance(current, self.NodeType)
            if self.DOUBLY:
                self.assertIs(current.prev, nodes[-1] if nodes else None,
                              'Incorrect prev link')
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
        if self.DOUBLY:
            current = linked._tail
            for node in reversed(nodes):
                self.assertIs(current, node, 'Backward traversal disagrees with forward chain')
                current = current.prev
            self.assertIsNone(current)
        return nodes

    @staticmethod
    def invoke(linked, op: str, args: list):
        """Explicit adapters for syntax-based operations; no eval or arbitrary code."""
        special = {
            'getitem': linked.__getitem__, 'setitem': linked.__setitem__,
            'delitem': linked.__delitem__, 'contains': linked.__contains__,
            'len': lambda: len(linked), 'bool': lambda: bool(linked),
            'iter': lambda: list(islice(linked, len(linked) + 1)),
        }
        if op in special:
            return special[op](*args)
        if op not in ARITIES:
            raise ValueError(f'Unknown operation: {op}')
        return getattr(linked, op)(*args)

    def test_json_snapshots(self) -> None:
        for raw_case in self.cases:
            # One subTest per scenario: a failed step stops its dependent steps.
            with self.subTest(case=raw_case['name']):
                case = deepcopy(raw_case)
                linked = self.List(case['input'])
                state = case['input']
                self.assert_list(linked, state)
                for number, step in enumerate(case['steps']):
                    context = f"{case['name']}: step {number}, {step['op']}{step['args']}"
                    before = self.assert_list(linked, state)
                    if 'raises' in step:
                        with self.assertRaises(ERRORS[step['raises']], msg=context):
                            self.invoke(linked, step['op'], step['args'])
                    else:
                        result = self.invoke(linked, step['op'], step['args'])
                        if step['op'] == 'reverse':
                            result_nodes = self.assert_list(result, step['expected_return'])
                            self.assertIsNot(result, linked)
                            self.assertTrue({id(n) for n in before}.isdisjoint(
                                id(n) for n in result_nodes), context)
                            self.assertEqual(self.assert_list(linked, state), before)
                            result = [node.value for node in result_nodes]
                        self.assertIs(type(result), type(step['expected_return']), context)
                        self.assertEqual(result, step['expected_return'], context)
                    self.assert_list(linked, step['expected'])
                    state = step['expected']

    def test_node_constructor(self) -> None:
        last = self.NodeType(20)
        first = self.NodeType(10, last)
        self.assertEqual(first.value, 10)
        self.assertIs(first.next, last)
        self.assertIsNone(last.next)
        if self.DOUBLY:
            self.assertIsNone(first.prev)
            last.prev = first
            middle = self.NodeType(15, next=last, prev=first)
            self.assertIs(middle.next, last)
            self.assertIs(middle.prev, first)

    def test_constructor_default_and_iterables(self) -> None:
        self.assert_list(self.List(), [])
        for source in ((10, 20), (x for x in (10, 20)), self.List([10, 20])):
            with self.subTest(source=type(source).__name__):
                self.assert_list(self.List(source), [10, 20])
        self.assert_list(self.List('ab'), ['a', 'b'])
        with self.assertRaises(TypeError):
            self.List(None)

    def test_instances_do_not_share_nodes(self) -> None:
        a = self.List([10, 20])
        b = self.List(a)
        an = self.assert_list(a, [10, 20])
        bn = self.assert_list(b, [10, 20])
        self.assertTrue({id(n) for n in an}.isdisjoint(id(n) for n in bn))
        a.append(30)
        self.assert_list(b, [10, 20])

    def test_extend_iterables(self) -> None:
        for source in ((20, 30), (x for x in (20, 30)), self.List([20, 30])):
            with self.subTest(source=type(source).__name__):
                linked = self.List([10])
                self.assertIsNone(linked.extend(source))
                self.assert_list(linked, [10, 20, 30])
        linked = self.List()
        linked.extend('ab')
        self.assert_list(linked, ['a', 'b'])

    def test_extend_self(self) -> None:
        for values in ([], [10], [10, 20, 30]):
            with self.subTest(values=values):
                linked = self.List(values)
                before = self.assert_list(linked, values)
                append = linked.append
                calls = 0
                def guarded_append(value):
                    nonlocal calls
                    calls += 1
                    self.assertLessEqual(calls, len(values), 'Endless self-extension')
                    return append(value)
                with patch.object(linked, 'append', side_effect=guarded_append):
                    self.assertIsNone(linked.extend(linked))
                after = self.assert_list(linked, values + values)
                self.assertEqual(after[:len(values)], before)
                self.assertTrue({id(n) for n in before}.isdisjoint(
                    id(n) for n in after[len(values):]))

    def test_iteration_and_independent_iterators(self) -> None:
        for values in ([], [10], [10, 20, 30]):
            linked = self.List(values)
            a, b = iter(linked), iter(linked)
            for value in values:
                self.assertEqual(next(a), value)
            with self.assertRaises(StopIteration):
                next(a)
            with self.assertRaises(StopIteration):
                next(a)
            self.assertEqual(list(islice(b, len(values) + 1)), values)
            self.assert_list(linked, values)

    def test_get_set_delete_all_valid_indices(self) -> None:
        for values in ([10], [10, 20, 30], list(range(8))):
            for index in range(-len(values), len(values)):
                with self.subTest(values=values, index=index):
                    linked, expected = self.List(values), values.copy()
                    before = self.assert_list(linked, expected)
                    self.assertEqual(linked[index], expected[index])
                    linked[index] = 99
                    expected[index] = 99
                    self.assertEqual(self.assert_list(linked, expected), before)
                    del linked[index]
                    del expected[index]
                    self.assert_list(linked, expected)

    def test_pop_all_indices_and_detachment(self) -> None:
        for values in ([10], [10, 20, 30], list(range(8))):
            for index in range(-len(values), len(values)):
                with self.subTest(values=values, index=index):
                    linked, expected = self.List(values), values.copy()
                    nodes = self.assert_list(linked, expected)
                    removed = nodes[index]
                    self.assertEqual(linked.pop(index), expected.pop(index))
                    self.assertIsNone(removed.next)
                    if self.DOUBLY:
                        self.assertIsNone(removed.prev)
                    linked.append(99)
                    self.assert_list(linked, expected + [99])

    def test_clear_detaches_nodes(self) -> None:
        linked = self.List([10, 20, 30])
        nodes = self.assert_list(linked, [10, 20, 30])
        self.assertIsNone(linked.clear())
        self.assert_list(linked, [])
        for node in nodes:
            self.assertIsNone(node.next)
            if self.DOUBLY:
                self.assertIsNone(node.prev)
        linked.append(99)
        self.assert_list(linked, [99])

    def test_search_identity_and_equality(self) -> None:
        # NaN is not equal to itself; identity still counts as a match.
        value = float('nan')
        linked = self.List([value, value])
        self.assertIn(value, linked)
        self.assertEqual(linked.index(value), 0)
        self.assertEqual(linked.count(value), 2)
        linked.remove(value)
        self.assertEqual(len(linked), 1)
        equal_but_distinct = {'score': 10}
        linked = self.List([{'score': 10}])
        self.assertEqual(linked.index(equal_but_distinct), 0)
        self.assertEqual(linked.count(equal_but_distinct), 1)
        self.assertIn(equal_but_distinct, linked)
        linked.remove(equal_but_distinct)
        self.assert_list(linked, [])

    def test_reverse_is_independent_shallow_copy(self) -> None:
        first, second = {'score': 10}, {'score': 20}
        linked = self.List([first, second])
        before = self.assert_list(linked, [first, second])
        result = linked.reverse()
        after = self.assert_list(result, [second, first])
        self.assertIsNot(result, linked)
        self.assertTrue({id(n) for n in before}.isdisjoint(id(n) for n in after))
        self.assertIs(result[0], second)
        self.assertIs(result[1], first)
        result[0]['score'] = 99
        self.assertEqual(linked[1]['score'], 99)
        result[0] = {'score': 50}
        result.append(30)
        self.assertEqual(self.assert_list(linked, [first, second]), before)
        self.assert_list(result, [{'score': 50}, first, 30])
        linked.prepend(5)
        self.assert_list(result, [{'score': 50}, first, 30])
        self.assert_list(linked, [5, first, second])

    def test_repr(self) -> None:
        for values in ([], [10], [10, 20, 30], ['hello', None]):
            linked = self.List(values)
            self.assertEqual(repr(linked), f'{self.List.__name__}({values!r})')
        linked = self.List()
        linked.append(linked)
        self.assertEqual(repr(linked), f'{self.List.__name__}([...])')
        linked.clear()

    def test_normalize_index_and_node_at(self) -> None:
        for size in range(9):
            values = list(range(size))
            linked = self.List(values)
            nodes = self.assert_list(linked, values)
            for index in range(-size, size):
                with self.subTest(size=size, index=index):
                    normalized = index if index >= 0 else size + index
                    self.assertEqual(linked._normalize_index(index), normalized)
                    self.assertIs(linked._node_at(index), nodes[normalized])
            for index in (-size - 1, size, -99, 99):
                for method in (linked._normalize_index, linked._node_at):
                    with self.assertRaises(IndexError):
                        method(index)

    def test_insertion_normalization_and_boundaries(self) -> None:
        for size in range(7):
            for index in range(-size - 3, size + 4):
                with self.subTest(size=size, index=index):
                    expected = list(range(size))
                    linked = self.List(expected)
                    expected.insert(index, 99)
                    position = expected.index(99)
                    self.assertEqual(linked._normalize_index(index, for_insert=True), position)
                    self.assertIsNone(linked.insert(index, 99))
                    self.assert_list(linked, expected)

    def test_bad_index_types_and_slices(self) -> None:
        for values in ([], [10, 20, 30]):
            for index in (None, '1', 1.5, [], {}, slice(None), slice(0, 2)):
                for op, args in [('getitem', [index]), ('setitem', [index, 99]),
                                 ('delitem', [index]), ('pop', [index]), ('insert', [index, 99])]:
                    with self.subTest(values=values, index=index, op=op):
                        linked = self.List(values)
                        with self.assertRaises(TypeError):
                            self.invoke(linked, op, args)
                        self.assert_list(linked, values)
                linked = self.List(values)
                for action in (lambda: linked._node_at(index),
                               lambda: linked._normalize_index(index),
                               lambda: linked._normalize_index(index, for_insert=True)):
                    with self.assertRaises(TypeError):
                        action()

    def test_seeded_mixed_operations(self) -> None:
        # Independent oracle: a Python list with two intentional API adaptations.
        randomizer = random.Random(20261013)
        linked, expected = self.List(), []
        operations = ('append', 'prepend', 'insert', 'pop', 'remove', 'setitem',
                      'delitem', 'index', 'count', 'extend', 'reverse', 'clear')
        for number in range(1000):
            op = randomizer.choice(operations)
            value = randomizer.randrange(-5, 6)
            index = randomizer.randrange(-len(expected) - 2, len(expected) + 3)
            args = {
                'append': [value], 'prepend': [value], 'insert': [index, value],
                'pop': [index], 'remove': [value], 'setitem': [index, value],
                'delitem': [index], 'index': [value], 'count': [value],
                'extend': [[value, value + 1]], 'reverse': [], 'clear': [],
            }[op]
            with self.subTest(step=number, op=op, args=args):
                try:
                    if op == 'prepend': result = expected.insert(0, value)
                    elif op == 'setitem': result = expected.__setitem__(*args)
                    elif op == 'delitem': result = expected.__delitem__(*args)
                    elif op == 'reverse': result = expected[::-1]
                    elif op == 'index':
                        try: result = expected.index(value)
                        except ValueError: result = None
                    else: result = getattr(expected, op)(*args)
                except (IndexError, ValueError) as exc:
                    with self.assertRaises(type(exc)):
                        self.invoke(linked, op, args)
                else:
                    actual = self.invoke(linked, op, args)
                    if op == 'reverse':
                        self.assert_list(actual, result)
                    else:
                        self.assertEqual(actual, result)
                self.assert_list(linked, expected)


class TestDoublyLinkedList(TestSinglyLinkedList):
    List = DoublyLinkedList
    NodeType = DoublyLinkedNode
    DOUBLY = True

    def test_reversed_iterator(self) -> None:
        for values in ([], [10], [10, 20, 30]):
            linked = self.List(values)
            before = self.assert_list(linked, values)
            a, b = reversed(linked), reversed(linked)
            self.assertIs(iter(a), a)
            for value in values[::-1]:
                self.assertEqual(next(a), value)
            with self.assertRaises(StopIteration):
                next(a)
            self.assertEqual(list(islice(b, len(values) + 1)), values[::-1])
            self.assertEqual(self.assert_list(linked, values), before)

    def test_backward_iteration_uses_prev_not_indexing(self) -> None:
        linked = self.List([10, 20, 30])
        with patch.object(linked, '_node_at', side_effect=AssertionError('Indexed traversal')):
            self.assertEqual(list(reversed(linked)), [30, 20, 10])

    def test_node_at_chooses_nearer_end(self) -> None:
        # Count link reads rather than timing; this checks the intended algorithm.
        class ProbeNode:
            reads = {'next': 0, 'prev': 0}
            def __init__(self, value):
                self.value = value
                self.forward = self.backward = None
            @property
            def next(self):
                type(self).reads['next'] += 1
                return self.forward
            @property
            def prev(self):
                type(self).reads['prev'] += 1
                return self.backward
        nodes = [ProbeNode(i) for i in range(8)]
        for i, node in enumerate(nodes):
            node.forward = nodes[i + 1] if i + 1 < len(nodes) else None
            node.backward = nodes[i - 1] if i else None
        linked = self.List()
        linked._head, linked._tail, linked._size = nodes[0], nodes[-1], len(nodes)
        for index, reads in [(0, {'next': 0, 'prev': 0}),
                             (1, {'next': 1, 'prev': 0}),
                             (6, {'next': 0, 'prev': 1}),
                             (7, {'next': 0, 'prev': 0})]:
            ProbeNode.reads = {'next': 0, 'prev': 0}
            self.assertIs(linked._node_at(index), nodes[index])
            self.assertEqual(ProbeNode.reads, reads)


if __name__ == '__main__':
    unittest.main(verbosity=2)