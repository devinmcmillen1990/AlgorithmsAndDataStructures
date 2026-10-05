import sys
from pathlib import Path


PROBLEM_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = PROBLEM_DIR.parent
sys.path.insert(1, str(PROJECT_ROOT))


import unittest
from utils.load_test_cases import load_test_cases
from lc_856_score_of_parentheses.s01_stack_recording_score_at_each_nest_level.solution import Solution as Solution1
from lc_856_score_of_parentheses.s02_recurse_letting_each_recursive_call_evaluate_one_level.solution import Solution as Solution2
from lc_856_score_of_parentheses.s03_count_depth_contributions_of_innermost_pairs.solution import Solution as Solution3


class TestScoreOfParentheses(unittest.TestCase):

    def test_stack_solution(self) -> None:
        cases = load_test_cases(PROBLEM_DIR / "test_cases.json")
        for case in cases:
            with self.subTest(name=case["name"], input=case["input"]):
                actual = Solution1().scoreOfParentheses(case["input"])
                self.assertEqual(actual, case["expected"])

    def test_recursive_solution(self) -> None:
            cases = load_test_cases(PROBLEM_DIR / "test_cases.json")
            for case in cases:
                with self.subTest(name=case["name"], input=case["input"]):
                    actual = Solution2().scoreOfParentheses(case["input"])
                    self.assertEqual(actual, case["expected"])

    def test_depth_counting_solution(self) -> None:
                cases = load_test_cases(PROBLEM_DIR / "test_cases.json")
                for case in cases:
                    with self.subTest(name=case["name"], input=case["input"]):
                        actual = Solution3().scoreOfParentheses(case["input"])
                        self.assertEqual(actual, case["expected"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
