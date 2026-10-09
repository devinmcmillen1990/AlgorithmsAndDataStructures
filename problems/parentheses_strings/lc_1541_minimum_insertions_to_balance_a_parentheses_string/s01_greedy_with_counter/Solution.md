<h1>1. Greedy With Counter</h2>

[Back to Problem](../LC_1541_MinimumInsertionsToBalanceParenthesesString.md)

<h2>Idea</h2>

Keep two counters
1. ```needed``` - how many additional ```)``` characters the processed portion still needs
   - ```(``` -> ```needed += 2```
   - ```)``` -> ```needed -= 1``` 
2. <strong>insertions</strong> - how many characters we have inserted so far

The tricky part is hanlding an unfinished ```))``` pair before another ```(``` appears.

<h2>Code</h2>

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

<h2>Time Complexity : </h2> 

<strong>O(n)</strong>, because each character is processed once

<h2>Space Complexity : </h2> 

<strong>O(1)</strong>, only counters are storing data

<h2>Categories</h2>

<ul>
    <li>Array</li>
    <li>Strings</li>
    <li>Greedy</li>
</ul>

[Back to Problem](../LC_1541_MinimumInsertionsToBalanceParenthesesString.md)