# 1. Counting Open and Closed Parentheses

[Back to Problem](../LC_921_MinimumAddToMakeParenthesesValid.md)

## Idea

Everytime we encounter a '(' then we increment the ```unmatched_open```.

When we encounter a ')'
  * If we have seen unmatched '(', then we decrement ```unmatched_open``` indicating that we have a closed pair.
  * Otherwise; we increment ```missing_open``` indicating that we have a ')' that was not closed.
Return the sum of ```missing_open``` and ```unmatched_open``` counted.

Assume every character is either '(' or ')' from the problem.

## Code

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

## Time Complexity

<strong>O(n)</strong>, because each character is processed once

## Space Complexity

<strong>O(h)</strong>, where 'h' is the maximum nesting depth; O(n) in the worst case

## Categories

<ul>
    <li>Array</li>
    <li>Strings</li>
</ul>
