<h1>1. Max Heap</h2>

[Back to Problem](../LC_2333_MinimumSumOfSquareDifferences.md)

<h2>Idea</h2>

Instead of squaring everytime we can keep track of the absolute value and square at the end.

For the <strong>Minimum Sum of Square Differences</strong> we can combine ```k1 + k2``` 

We will load the differences into a <strong>Max Heap</strong> and we keep making edits for each ```k``` edits that we have available, updating the heap whenever we make an edit.

<strong>Important limitation:</strong> this version is correct, but not suitable for the worst-case constraints. Each individual budget can reach \(10^9\), so processing one operation per iteration can require billions of iterations.

<h2>Code</h2>

```python
import heapq


class Solution:
    def minSumSquareDiff(self, nums1: list[int], nums2: list[int], k1: int, k2: int) -> int:
        differences = [
            abs(a - b)                              # deal with absolute value instead of squaring. don't need to square until the end
            for a, b in zip(nums1, nums2)           # zip returns an iterator or tuples
        ]
        # we can combine k1 and k2 for min diff. Any positive difference can be reduced by editing either array
        k = k1 + k2                                 
        if k >= sum(differences): return 0          # if (k1+k2) is greater than the total current sum, then we can edit it down to 0       
        heap = [-d for d in differences]            # create max heap. max heap is implemented with negative values
        heapq.heapify(heap)                         # build the heap in linear time to order by max sums
        for _ in range(k):                          # iterate while we can edit
            largest = -heapq.heappop(heap)          # grab the current max diff in the heap. remember to negate when popping from heap
            heapq.heappush(heap, -(largest - 1))    # after modifying the current max diff push it back into the heap
        return sum(d**2 for d in heap)              # return the sum square diff for the current state of the heap

```

<h2>Time Complexity : </h2> 

<strong>O(n + Klog(n))</strong>, ```n``` is the size of the heap and ```K``` is the number of possible edits after combining ```k1+k2```

<h2>Space Complexity : </h2> 

<strong>O(n)</strong>, for the heap

<h2>Categories</h2>

<ul>
    <li>Array</li>
    <li>Strings</li>
    <li>Heap</li>
</ul>

[Back to Problem](../LC_2333_MinimumSumOfSquareDifferences.md)