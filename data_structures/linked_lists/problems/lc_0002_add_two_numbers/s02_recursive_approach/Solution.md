# 1. Iterative Approach

[Back to Problem](../AddTwoNumbers.md)

## Idea

Similar to [1. Iterative Approach](../s01_iterative_approach/Solution.md) but instead of iteratively moving Linked List pointers we leverage recursion to build the linked list.

## Code

```python
class Solution:
    def addTwoNumbers(self, l1: ListNode|None, l2: ListNode|None) -> ListNode|None:
        def add(a: ListNode|None, b: ListNode|None, carry: int) -> ListNode|None:
            if a is None and b is None and carry == 0:
                return None                         # Exit condition
            digit1 = a.val if a is not None else 0  
            digit2 = b.val if b is not None else 0
            current_sum = digit1 + digit2 + carry
            next_carry = current_sum // 10          # get next carry over
            digit = current_sum % 10                # calculate current digit of the sum
            node = ListNode(digit)                  # assign to the current node
            node.next = add(                        # set the next node recursively
                a.next if a is not None else None,  # move a (l1)
                b.next if b is not None else None,  # move b (l2)
                next_carry)
            return node                             # return from recursion
        return add(l1, l2, 0)
```

## Time Complexity 

<strong>O(m+n)</strong>, where "m" is the length of "l1" and "n" is the length of "l2"

## Space Complexity

<strong>O(n)</strong>, where "n" is the length of the longest linked list

## Categories
- Singly Linked List
- Recursion

[Back to Problem](../AddTwoNumbers.md)