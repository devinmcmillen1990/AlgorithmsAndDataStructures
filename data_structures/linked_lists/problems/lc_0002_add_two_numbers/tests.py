from __future__ import annotations

import sys
import unittest
from pathlib import Path


PROBLEM_DIR = Path(__file__).resolve().parent

for parent in PROBLEM_DIR.parents:
    if (parent / "utils" / "load_test_cases.py").is_file():
        PROJECT_ROOT = parent
        break
else:
    raise RuntimeError(
        "Could not find utils/load_test_cases.py above the problem directory."
    )

sys.path.insert(0, str(PROBLEM_DIR))
sys.path.insert(1, str(PROJECT_ROOT))

from utils.load_test_cases import load_test_cases
from data_structures.linked_lists.problems.lc_0002_add_two_numbers.common.list_node import ListNode
from s01_iterative_approach.solution import Solution as Solution1
from s02_recursive_approach.solution import Solution as Solution2


class TestMinimumInsertionsToBalanceParenthesesString(unittest.TestCase):

    def test_iterative_solution(self) -> None:
        cases = load_test_cases(PROBLEM_DIR / "test_cases.json")
        for case in cases:
            with self.subTest(name=case["name"], input=case["input"]):
                l1 = self.list_to_linked_list(case["input"]["l1"])
                l2 = self.list_to_linked_list(case["input"]["l2"])
                actual = Solution1().addTwoNumbers(l1, l2)
                self.assertEqual(
                    self.linked_list_to_list(actual),
                    case["expected"]
                )

    def test_recursive_solution(self) -> None:
        cases = load_test_cases(PROBLEM_DIR / "test_cases.json")
        for case in cases:
            with self.subTest(name=case["name"], input=case["input"]):
                l1 = self.list_to_linked_list(case["input"]["l1"])
                l2 = self.list_to_linked_list(case["input"]["l2"])
                actual = Solution2().addTwoNumbers(l1, l2)
                self.assertEqual(
                    self.linked_list_to_list(actual), 
                    case["expected"]
                )

    @staticmethod
    def list_to_linked_list(values: list[int]) -> ListNode | None:
        dummy = ListNode()
        tail = dummy
        for value in values:
            tail.next = ListNode(value)
            tail = tail.next
        return dummy.next

    @staticmethod
    def linked_list_to_list(head: ListNode | None) -> list[int]:
        values: list[int] = []
        seen: set[int] = set()
        while head is not None:
            node_id = id(head)
            if node_id in seen:
                raise AssertionError("The returned linked list contains a cycle.")
            seen.add(node_id)
            values.append(head.val)
            head = head.next
        return values


if __name__ == "__main__":
    unittest.main(verbosity=2)