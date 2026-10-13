import sys
from pathlib import Path


PROBLEM_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = PROBLEM_DIR.parent.parent.parent
sys.path.insert(1, str(PROJECT_ROOT))


import unittest
from utils.load_test_cases import load_test_cases
from problems.sum_differences.lc_2333_minimum_sum_of_square_differences.s01_max_heap.solution import Solution as Solution1
from problems.sum_differences.lc_2333_minimum_sum_of_square_differences.s02_frequency_buckets.solution import Solution as Solution2
from problems.sum_differences.lc_2333_minimum_sum_of_square_differences.s03_binary_search_for_a_final_height.solution import Solution as Solution3
from problems.sum_differences.lc_2333_minimum_sum_of_square_differences.s04_sort_and_lower_groups_together.solution import Solution as Solution4


class TestMinimumSumOfSqureDifferences(unittest.TestCase):

    def test_max_heap_solution(self) -> None:
        cases = load_test_cases(PROBLEM_DIR / "test_cases.json")
        for case in cases:
            # Snapshot data
            name = case["name"]
            nums1, nums2 = case["input_nums1"], case["input_nums2"]
            k1, k2 = case["input_k1"], case["input_k2"]
            large_running = case["large_running"]
            expected = case["expected"]
            # Tests
            with self.subTest(name, nums1=nums1, nums2=nums2, k1=k1, k2=k2):
                if large_running == False:                  # Skip for the heap tests
                    actual = Solution1().minSumSquareDiff(
                        nums1=nums1,
                        nums2=nums2,
                        k1=k1,
                        k2=k2)
                    self.assertEqual(actual, expected)

    def test_frequency_buckets_solution(self) -> None:
        cases = load_test_cases(PROBLEM_DIR / "test_cases.json")
        for case in cases:
            # Snapshot data
            name = case["name"]
            nums1, nums2 = case["input_nums1"], case["input_nums2"]
            k1, k2 = case["input_k1"], case["input_k2"]
            expected = case["expected"]
            # Tests
            with self.subTest(name, nums1=nums1, nums2=nums2, k1=k1, k2=k2):
                actual = Solution2().minSumSquareDiff(
                    nums1=nums1,
                    nums2=nums2,
                    k1=k1,
                    k2=k2)
                self.assertEqual(actual, expected)

    # def test_binary_search_for_final_height_solution(self) -> None:
    #         cases = load_test_cases(PROBLEM_DIR / "test_cases.json")
    #         for case in cases:
    #             with self.subTest(name=case["name"], input=["input"]):
    #                 actual = Solution3().minSumSquareDiff(case["input"])
    #                 self.assertEqual(actual, case["expected"])

    # def test_sort_and_lower_groups_together_solution(self) -> None:
    #         cases = load_test_cases(PROBLEM_DIR / "test_cases.json")
    #         for case in cases:
    #             with self.subTest(name=case["name"], input=["input"]):
    #                 actual = Solution4().minSumSquareDiff(case["input"])
    #                 self.assertEqual(actual, case["expected"])


if __name__ == "__main__":
    unittest.main(verbosity=2)