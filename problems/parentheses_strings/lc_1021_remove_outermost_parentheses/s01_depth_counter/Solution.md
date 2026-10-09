<h1>1. Depth Counter</h2>

[Back to Problem](../LC_1021_RemoveOutermostParentheses.md)

<h2>Idea</h2>

Key concept is to track how many ```(``` are currently unmatched.

We will record the current character in the string if 
* we see a ```(``` and ```depth > 0``` 
  * we record at this point because depth being greater than zero means we are in a nesting
* we see a ```)``` and ```depth > 0```
  * we record at this point because when entering this block the depth would have to be 1 or more meaning that this current ```)``` is part of an inner pair

<h2>Code</h2>

```python
class Solution:
    def removeOuterParentheses(self, s: str) -> str:
        result = []
        depth = 0                       # Used to track how many parentheses are currently unmatched
        for char in s:
            if char == '(':             # Encounter '(' - Opening
                if depth > 0:           # check depth before (++) depth. means we have already seen a '('
                    result.append(char) # append '(' because this parenthesis is nested because depth > 0
                depth += 1              # (++) depth each iteration we encounter '('
            else:                       # Encounter ')' - Closing
                depth -= 1              # (--) depth each iteration we encounter ')'
                if depth > 0:           # check depth after incrementing. if depth is 0 then this ')' closes the final parenthesis
                    result.append(char) # append ')' to the output result
        return "".join(result)
```

<h2>Time Complexity : </h2> 

<strong>O(n)</strong>, because each character is processed once

<h2>Space Complexity : </h2> 

<strong>O(1)</strong>, only counters are storing data

<h2>Categories</h2>

<ul>
    <li>Array</li>
    <li>Strings</li>
    <li>Stack</li>
</ul>

[Back to Problem](../LC_1021_RemoveOutermostParentheses.md)