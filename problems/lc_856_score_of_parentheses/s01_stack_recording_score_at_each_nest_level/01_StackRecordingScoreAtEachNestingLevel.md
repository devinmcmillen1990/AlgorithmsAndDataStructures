<h1>1. Stack Recording Score at each Nesting Level</h2>

[Back to Problem](../LC_856_ScoreOfParentheses.md)

<h2>Idea</h2>

Whenever we open a pair of parentheses, start tracking a new score. When we close it, calculate that group's score and add it to its parent.

<h2>Code</h2>

```python
class Solution:
    def scoreOfParentheses(self, s: str) -> int:
        stack = [0]                         # Set first entry to '0'. This will track the score of the whole expression
        for char in s:
            if char == '(':                 # Encounter '(' - Opening
                stack.append(0)             # start a new group with the innermost score '0'
            else:                           # Encounter ')' - Closing
                inner = stack.pop()         # get the score inside the group we are closing
                if inner == 0:              # nothing inside means this group is '()'
                    group_score = 1         
                else:
                    group_score = 2 * inner # wrapping nonempty group to its parent's score
                stack[-1] += group_score    # add this completed group to its parent's score
        return stack[0]
```

<h2>Time Complexity : </h2> 

<strong>O(n)</strong>, because each character is processed once

<h2>Space Complexity : </h2> 

<strong>O(h)</strong>, where 'h' is the maximum nesting depth; O(n) in the worst case

<h2>Categories</h2>

<ul>
    <li>Array</li>
    <li>Strings</li>
    <li>Stack</li>
</ul>
