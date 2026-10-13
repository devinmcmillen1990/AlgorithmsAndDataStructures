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


'''
Example - nums1=[1,2,3,4], nums2=[2,10,20,19], k1=0, k2=0

1. calculate edit budget (k1+k2) [currently k==0]
2. initialize total_diff and max_diff to 0
3. Loop over combination of nums1 and nums2
    a. Iteration 0 (1, 2)
        -- difference=abs(1-2) [currently difference==1]
        -- (+difference)total_diff [currently total_diff==1, max_diff==0]
        -- max_diff=difference -> difference > max_diff [currently max_diff=1]
    b. Iteration 1 (2, 10)
        -- difference=abs(2-10) [currently difference==8]
        -- (+difference)total_diff [currently total_diff==9, max_diff==1]
        -- max_dif=difference -> difference > max_diff [currently max_diff==9]
    c. Iteration 2 (3, 20)
        -- difference=abs(3-20) [currently difference==17]
        -- (+difference)total_diff [currently total_diff==26, max_diff==9]
        -- max_diff=difference -> difference > max_diff [currently max_diff==17]
    d. Iteration 3 (4, 19)
        -- difference=abs(4-19) [currently difference==15]
        -- (+difference)total_diff [currently total_diff==51, max_diff==15]
        -- max_diff=max_diff -> max_diff > difference [currently max_diff==17]
4. skip if block because k < total_diff [currently k==2, total_diff==51]
5. create frequency buckets all starting at 0 (size of array is the "max_diff+1" because the differences are used as indexes for the array)
6. iterate over the combination of nums1 and nums2 to calculate the frequency that each difference occurs originally. 
    * [currently counts==[0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,1]]
7. iterate from max_diff, decreasing, because the right side of the array will have the largest differences
    a. Iteration 0 (difference==17)
        -- moves=counts[difference]     -> counts[differences]<k [currently moves==0,k==0,counts[17]==1]
        -- (-moves)counts[difference]   -> moves==0, no change [currently counts[17]==1]
        -- (+moves)counts[difference-1] -> moves==0, no change [currently counts[16]==1, counts[17]==0]
        -- (--)k                        -> moves==0, no change [curently k==0]
        -- enter if block because k==0 and stop looping
    * [currently counts==[0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,1]]
8. return the sum of of the counts of the differences by their square. [(1^2)+(8^2)+(15^2)+(17^2)] -> [returns 579]
========================================================================================================================

Example - nums1=[1,4,10,12], nums2=[5,8,6,9], k1=1, k2=1

1. calculate edit budget (k1+k2) [currently k==2]
2. initialize total_diff and max_diff to 0
3. Loop over combination of nums1 and nums2 to find max number of differences
    a. Iteration 0 (1, 5)
        -- difference=abs(1-5) [currently difference==4]
        -- (+difference)total_diff [currently total_diff==4, max_diff==0]
        -- max_diff=difference -> difference > max_diff [currently max_diff==4]
    b. Iteration 1 (4, 8)
        -- difference=abs(4-8) [currently difference==4]
        -- (+difference)totaldiff [currently total_diff==8, max_diff==4]
        -- max_diff=difference -> difference==max_diff so both work [currently max_diff==4]
    c. Iteration 2 (10, 6)
        -- difference=abs(10-6) [currently difference==4]
        -- (+difference)total_diff [currently total_diff==12, max_diff==4]
        -- max_diff=difference -> difference==max_diff so both work [currently max_diff==4]
    d. Iteration 3 (12, 9)
        -- difference=abs(12-9) [currently difference==3]
        --(+difference)total_diff [currently total_diff==15, max_diff==4]
        -- max_diff=difference -> difference < max_diff [currently max_diff==3]
4. skip if block because k < total_diff [currently k==2, total_diff==15]
5. create frequency buckets all starting at 0 (size of array is the "max_diff+1" because the differences are used as indexes for the array)
6. iterate over the combination of nums1 and nums2 to calcaulte the frequency that each difference occurs originally. 
    * [currently counts==[0,0,0,1,3]]
7. iterate from max_diff, decreasing, because the right side of the array will have the largest differences
    a. Iteration 0 (difference==4)
        -- moves=k                      -> counts[difference]>k [currently moves==2,k==2,counts[4]==3]
        -- (-moves)counts[difference]   -> make edit(s) on the current largest difference [currently counts[4]==1]
        -- (+moves)counts[difference-1] -> we edited counts[difference] so now its difference equals counts[difference-1] [currently counts[4]==1, counts[3]==3]
        -- (-moves)k                    -> made an edit [currently k==0]
        -- enter if block because k==0 and stop looping
    * [currently counts==[0,0,0,3,1]]
8. return the sum of of the counts of the differences by their square. [3*(3^2)+(4^2)] -> [returns 43]
'''