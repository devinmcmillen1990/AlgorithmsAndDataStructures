class Solution:
    def minSumSquareDiff(self, nums1: list[int], nums2: list[int], k1: int, k2: int) -> int:
        differences = [
            abs(a-b)
            for a, b in zip(nums1, nums2)
        ]
        k = k1 + k2
        if k >= sum(differences): return 0
        low, high = 0, max(differences)
        while low < high:
            threshold = (low + high) // 2
            required = sum(
                max(0, diff-threshold)
                for diff in differences
            )