<h1>2. Greedy Solution that explicitly consumes )) Pairs</h2>

[Back to Problem](../LC_1541_MinimumInsertionsToBalanceParenthesesString.md)

<h2>Idea</h2>

Maintain ```open_count``` - number of unmatched opening parentheses

Whenever we encounter ```)```:
1. Consume ```))``` when the next character is also ```)```. Otherwise, insert its missing partner
2. Match that closing pair with an available ```(```. When no opening is available, insert one.

<h2>Code</h2>

```python
class Solution:
    def minInsertions(self, s: str) -> int:
        insertions = 0                                  # tracks insertions made so far
        open_count = 0                                  # tracks # of unmatched ')'
        i = 0                                           
        while i < len(s):
            if s[i] == '(':                             # Encountered '(' - Opening
                open_count += 1                         # (++) open_count
                i += 1                                  # (++) i
            else:                                       # Encountered ')' - Closing
                if i + 1 < len(s) and s[i + 1] == ')':  # Check if next char forms '))'
                    i += 2                              # (i+=2), closing set already exists
                else:                                   # following char is actually a '(', so only 1 ')' exists
                    insertions += 1                     # (++) insertions, since we have only 1 ')' insert its partner
                    i += 1                              
                if open_count > 0:                      # match the closing pair with an opening since we encountered ')'
                    open_count -= 1
                else:                                   # match not found
                    insertions += 1                     # (++) insertions, requires insert a '(' before this closing pair
        return insertions + 2 * open_count

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
