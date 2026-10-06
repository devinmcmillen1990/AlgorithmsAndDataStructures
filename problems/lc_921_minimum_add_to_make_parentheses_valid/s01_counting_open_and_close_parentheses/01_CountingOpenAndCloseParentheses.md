<h1>1. Counting Open and Closed Parentheses</h2>

[Back to Problem](../LC_921_MinimumAddToMakeParenthesesValid.md)

<h2>Idea</h2>

Everytime we encounter a '(' then we increment the ```unmatched_open```.

When we encounter a ')'
  * If we have seen unmatched '(', then we decrement ```unmatched_open``` indicating that we have a closed pair.
  * Otherwise; we increment ```missing_open``` indicating that we have a ')' that was not closed.
Return the sum of ```missing_open``` and ```unmatched_open``` counted.

Assume every character is either '(' or ')' from the problem.

<h2>Code</h2>

```python
class Solution:
    def minAddToMakeValid(self, s: str) -> int:
        unmatched_open, missing_open = 0, 0
        for char in s:
            if char == '(':             # Encounter '(' - Opening
                unmatched_open += 1     # (++) unmatched_open
            elif unmatched_open > 0:    # Encounter ')' - Closing AND we tracked some unmatched ')'
                unmatched_open -= 1     # (--) unmatched_open because we have a ')' for the tracked unmatched '('
            else:                       # Encounter ')' - Closing AND we have no unmatched ')'
                missing_open += 1       # (++) missing_open because this means that we have a '(' and don't have an unmatched ')'.
        return missing_open + unmatched_open
```

<h2>Time Complexity : </h2> 

<strong>O(n)</strong>, because each character is processed once

<h2>Space Complexity : </h2> 

<strong>O(h)</strong>, where 'h' is the maximum nesting depth; O(n) in the worst case

<h2>Categories</h2>

<ul>
    <li>Array</li>
    <li>Strings</li>
</ul>
