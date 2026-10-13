# 2. Frequency Buckets

[Back to Problem](../LC_2333_MinimumSumOfSquareDifferences.md)

## Idea

1. First, we need to get ```max_diff``` that will be used to determine the number of indexes for our frequency buckets
   -- We'll also use ```total_diff``` to gather the total number of edits and return 0 if there are more edits than we need to get a minimum square sum.
2. We'll initialize the <strong>Frequency Buckets</strong> with all frequencies starting at ```0```.
   -- Each index of the ```counts[]``` is the absolute value difference and the value at the index is the count of occurrence.
3. We'll load the initial frequencies into the buckets
   ```python
   for a, b in zip(nums1, nums2):
            difference = abs(a-b)
            counts[difference] += 1   
   ```
4. Then we'll go from ```max_diff``` (which is the highest recorded difference) and we'll perform as many edits for each difference to get them to ```0```.
   -- if we run out of edits, ```k```, then we stop
5. We'll then square all the values in counts and multiply them by the counts that we have after making these edits.
   
## Code

```python
class Solution:
    def minSumSquareDiff(self, nums1: list[int], nums2: list[int], k1: int, k2: int) -> int:
        k = k1 + k2                                 # edit budget
        total_diff, max_diff = 0, 0
        for (a,b) in zip(nums1, nums2):
            difference = abs(a-b)                   # only tracking abs value and not squaring until the end
            total_diff += difference                # (+d)total_diff -> the total available differences for this iteration of (a,b)
            max_diff = max(max_diff, difference)    # track the highest difference
        if k >= total_diff:                         # if the number of edits is greater than the current sum then it will be 0
            return 0
        counts = [0] * (max_diff + 1)               # frequency buckets - count how often each difference occurs, instead of storing in a heap
        for a, b in zip(nums1, nums2):              # load frequencies (Index for counts is the difference and the value is the count)
            difference = abs(a-b)
            counts[difference] += 1                 # (++)count[difference] for each difference that we have
        for difference in range(max_diff, 0, -1):   # decrease starting from max_diff (backwards because the max sums will be on the right side of the array)
            moves = min(k, counts[difference])      # how many differences with value "diff" to reduce by 1 edit
            counts[difference] -= moves             # make the edits to the current bucked "diff"
            counts[difference-1] += moves           # move those edits to the previous bucket -> "diff-1"
            k -= moves                              # (--)k -> edit budge
            if k == 0: break                        # edit budget exhausted, stop looping
                
        return sum(                                 # return sum of square differences
            count * d * d                           # square the differences
            for d, count in enumerate(counts)
        )
```

## Time Complexity

<strong>O(n+m)</strong>, where ```n``` is the length of ```num1``` or ```nums2```, and ```m``` is the absolute value for the max difference between elements in ```nums1``` and ```nums2```

## Space Complexity

<strong>O(m+1)</strong>, where ```m``` is the absolute value max difference

## Categories

<ul>
    <li>Array</li>
    <li>Strings</li>
    <li>Buckets</li>
</ul>

[Back to Problem](../LC_2333_MinimumSumOfSquareDifferences.md)