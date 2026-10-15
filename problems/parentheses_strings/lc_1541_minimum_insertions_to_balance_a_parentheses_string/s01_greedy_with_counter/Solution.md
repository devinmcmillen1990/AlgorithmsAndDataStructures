# 1. Greedy With Counter

[Back to Problem](../LC_1541_MinimumInsertionsToBalanceParenthesesString.md)

## Idea

Keep two counters
1. ```needed``` - how many additional ```)``` characters the processed portion still needs
   - ```(``` -> ```needed += 2```
   - ```)``` -> ```needed -= 1``` 
2. <strong>insertions</strong> - how many characters we have inserted so far

The tricky part is hanlding an unfinished ```))``` pair before another ```(``` appears.

## Code

```python
class Solution:
    def minInsertions(self, s: str) -> int:
        insertions = 0              # tracks insertions made so far
        needed = 0                  # tracks the number of ')' needed
        for char in s:
            if char == '(':         # Encounter '(' - Opening
                if needed % 2 == 1: # we encountered a ')' before the current '(' -> {*()>}
                    insertions += 1 # need to insert a ')'
                    needed -= 1     # (--) needed because we close a pair before starting another opening
                needed += 2         # new '(' requires 2 closing parentheses
            else:                   # Encounter ')' - Closing
                needed -= 1         # (--) needed because needed the number of ')' still needed
                if needed < 0:      # there was no '(' available for the current ')'
                    insertions += 1 # insert '(' before the current ')'
                    needed = 1      # the insert above needs one more ')' to close
        return insertions + needed  # return (insertions made) + (number of needed ')')
```

## Time Complexity 

<strong>O(n)</strong>, because each character is processed once

## Space Complexity

<strong>O(1)</strong>, only counters are storing data

## Categories
- Array
- Strings
- Greedy

[Back to Problem](../LC_1541_MinimumInsertionsToBalanceParenthesesString.md)