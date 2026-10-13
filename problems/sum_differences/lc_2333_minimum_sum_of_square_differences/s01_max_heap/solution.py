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


'''
Example - nums1=[1,2,3,4], nums2=[2,10,20,19], k1=0, k2=0

1. calculate absolute value differences [currently differences==[1,8,17,15] ]
2. combine k1 and k2 [currently k==0]
3. skip if block because k <= sum(differences) [currently k==0 and sum(differences)==41]
4. create max heap [currently heap==[-1,-8,-17,-15] ]
5. heapify [currently heap==[-17,-15,-8,-1] ]
6. iterate "k" times - skip loop because no edits [currently k==0]
7. square all of the sums and return the result [returns 579]

========================================================================================================================

Example - nums1=[1,4,10,12], nums2=[5,8,6,9], k1=1, k2=1

1. calculate absolute value differences [currently differences==[4,4,4,3] ]
2. combine k1 and k2 [currently k==2]
3. skip if block because k <= sum(differences) [currently k==0 and sum(differences)==15]
4. create max heap [currently heap==[-4,-4,-4,-3] ]
5. heapify [currently heap==[-4,-4,-4,-3] ]
6. iterate "k" times
    -- Iteration 1
        * get largest from max heap [currently largest=4]
        * make an edit [largest-=1] and heappush the value back [currently heap==[-4,-4,-3,-3] ]
    -- Iteration 2
        * get largest from max heap [currently largest=4]
        * make an edit [largest-=1] and heappush the value back [currently heap==[-4,-3,-3,-3] ]
7. square all of the sums and return the result [returns 43]
'''