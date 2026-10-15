# 1. Iterative Approach

[Back to Problem](../AddTwoNumbers.md)

## Idea

First we set and ```output``` ListNode and a ```current``` node for tracking the current digit of the Linked-List number.

We then loop while the following conditions are true
- ```l1 is not None```
- ```l2 is not None```
- ```carry != 0```

For each iteration we set the current digit sum, ```total```, equal to ```carry``` so that we can perform the carry over addition on each iteration. We then add then move ```l1.val``` and ```l2.val``` to ```total``` if they are available. 

After we add up the ```total``` for this iteration, we then need to get
1. the single digit for the next ```ListNode()``` value
2. any carry over values for the next iteration

We then assign the value to a ```ListNode(digit)``` for ```current.next``` to track the digit we just calculated. Finally, we move the current pointer to the node we just created and iterate again until the while boolean expression no longer satisfy the loop conditions.

## Code

```python
class Solution:
    def addTwoNumbers(self, l1: ListNode|None, l2: ListNode|None) -> ListNode|None:
        output = ListNode(0)                # Place holder ListNode(0)
        current = output
        carry = 0                           # manages the carry for each iteration if the total>=10
        while l1 is not None or l2 is not None or carry != 0:
            total = carry                   # basically -> total=0 (start each iteration) then total+=carry (add the carry)
            if l1 is not None:
                total += l1.val             # (+l1)total
                l1 = l1.next                # move l1
            if l2 is not None:
                total += l2.val             # (+l2)total
                l2 = l2.next                # move l2
            carry = total // 10             # get the carry over from the total if total>=10
            digit = total % 10              # mod10 the total to get the remainder
            current.next = ListNode(digit)  # assign to the next node
            current = current.next          # move current
        return output.next                  # return output.next because the first node is a placeholder
```

## Time Complexity 

<strong>O(m+n)</strong>, where "m" is the length of "l1" and "n" is the length of "l2"

## Space Complexity

<strong>O(n)</strong>, where "n" is the length of the longest linked list

## Categories
- Singly Linked List
- Recursion

[Back to Problem](../AddTwoNumbers.md)