import sys
from pathlib import Path


PROBLEM_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = PROBLEM_DIR.parent.parent.parent
sys.path.insert(1, str(PROJECT_ROOT))


import unittest
from utils.load_test_cases import load_test_cases
from problems.parentheses_strings.lc_1541_minimum_insertions_to_balance_a_parentheses_string.s01_greedy_with_counter.solution import Solution as Solution1
from problems.parentheses_strings.lc_1541_minimum_insertions_to_balance_a_parentheses_string.s02_greedy_that_explicitly_consumes_closing_pairs.solution import Solution as Solution2


class TestMinimumInsertionsToBalanceParenthesesString(unittest.TestCase):

    def test_greedy_with_counter_solution(self) -> None:
        cases = load_test_cases(PROBLEM_DIR / "test_cases.json")
        for case in cases:
            with self.subTest(name=case["name"], input=case["input"]):
                actual = Solution1().minInsertions(case["input"])
                self.assertEqual(actual, case["expected"])

    def test_greedy_that_explicitly_consumes_closing_pairs_solution(self) -> None:
        cases = load_test_cases(PROBLEM_DIR / "test_cases.json")
        for case in cases:
            with self.subTest(name=case["name"], input=["input"]):
                actual = Solution2().minInsertions(case["input"])
                self.assertEqual(actual, case["expected"])


if __name__ == "__main__":
    unittest.main(verbosity=2)