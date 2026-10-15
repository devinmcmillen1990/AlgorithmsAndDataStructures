from __future__ import annotations

import sys
from pathlib import Path


PROBLEM_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(PROBLEM_DIR))

from data_structures.linked_lists.problems.lc_0002_add_two_numbers.common.list_node import ListNode


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


'''
Example 1 - l1=2->4->3, l2=5->6->4

1. output=ListNode(0), which is a placeholder root for current
2. initialize tracking variables                        [current==ListNode(0), carry==0]
3. while loop over l1 and l2
    a. Iteration 0                                      [l1==ListNode(2), l2==ListNode(5)]
        -- total=carry for each iteration               [total==0]
        -- enter if block because l1 is not None        [l1==ListNode(2)]
            * (+l1.val)total then move l1               [total==2]
        -- enter if block because l2 is not None        [l2==ListNode(5)]
            * (+l2.val)total then move l2               [total==7]
        -- calculate carry over                         [carry==0]
        -- calculate digit after carry                  [digit==7]
        -- set the value as the next node for current   [current==ListNode(0), current.next==ListNode(7)]
        -- move current                                 [current==ListNode(7)]
    b. Iteration 1                                      [l1==ListNode(4), l2==ListNode(6)]
        -- total=carry for each iteration               [total==0]
        -- enter if block because l1 is not None        [l1==ListNode(4)]
            * (+l1.val)total then move l1               [total==4]
        -- enter if block because l2 is not None        [l2==ListNode(6)]
            * (+l2.val)total then move l2               [total==10]
        -- calculate carry over                         [carry==1]
        -- calculate digit after carry                  [digit==0]
        -- set the value as the next node for current   [current==ListNode(7), current.next==ListNode(0)]
        -- move current                                 [current==ListNode(0)]
    c. Iteration 2                                      [l1==ListNode(3), l2==ListNode(4)]
        -- total=carry                                  [total==1]
        -- enter if block because l1 is not None        [l1==ListNode(3)]
            * (+l1.val)total then move l1               [total==4]
        -- enter if block because l2 is not None        [l2==ListNode(4)]
            * (+l2.val)total then move l2               [total==8]
        -- calculate carry over                         [carry==0]
        -- calculate digit after carry                  [digit==8]
        -- set the value as the next node for current   [current==ListNode(0), current.next==ListNode(8)]
        -- move current                                 [current==ListNode(8)]
    d. Iteration 3 l1==None, l2==None
        -- exit loop
4. Return output.next, remembering the placeholder      [returns 7->0->8]
'''
