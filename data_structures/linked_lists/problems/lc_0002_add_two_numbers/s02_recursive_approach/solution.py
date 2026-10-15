from __future__ import annotations

import sys
from pathlib import Path


PROBLEM_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(PROBLEM_DIR))

from data_structures.linked_lists.problems.lc_0002_add_two_numbers.common.list_node import ListNode


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


'''
Example 1 - l1=2->4->3, l2=5->6->4

Recursion 0                                         [a==ListNode(2), b==ListNode(5)]
1. skip if block because neither a nor a is None    [a==ListNode(2), b==ListNode(5)]
2. digit1=a.val -> l1.val==2                        [digit1==2]
3. digit2=b.val -> l2.val==5                        [digit2==5]
4. calculate current sum                            [current_sum==7]
5. calculate carry over                             [next_carry==0]
6. calculate digit after carry                      [digit==7]
7. assign digit to current node                     [node==ListNode(7)]
8. set node.next recursively

Recursion 1                                         [a==ListNode(4), a==ListNode(6)]
1. skip if block because neither a nor b is None    [a==ListNode(4), b==ListNode(6)]
2. digit1=a.val -> a.val==4                         [digit1==4]
3. digit2=b.val -> b.val==6                         [digit2==6]
4. calculate current sum                            [current_sum==10]
5. calculate carry over                             [next_carry==1]
6. calculate digit after carry                      [digit==0]
7. assign digit to current node                     [node==ListNode(0)]
8. set node.next recursively                        

Recursion 2
1. skip if block becuase neither a nor b is None    [a==ListNode(3), b==ListNode(4)]
2. digit1=a.val -> a.val==4                         [digit1==3]
3. digit2=b.val -> b.val==6                         [digit2==4]
4. calculate current sum                            [current_sum==8]
5. calculate carry over                             [next_carry==0]
6. calculate digit after carry                      [digit==8]
7. assign digit to current node                     [node==ListNode(8)]
8. set node.next recursively   

Recursion 3
1. enter if block because a nd b are None and carry == 0

Return result of recursion [returns 7->0->8]
'''
