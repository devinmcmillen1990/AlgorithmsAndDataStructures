# 1. Stack Solution

[Back to Problem](../LC_1021_RemoveOutermostParentheses.md)

## Idea

Similar to the last solution, except we use the length of the stack to determine if we should record inner parenthesis.

We will record the current character in a string if
* we see a ```(``` and the ```stack``` is not empty
  * we record at this point because ```(```'s in a stack indicate that we are in a nesting
* we see a ```)``` and the ```stack``` is not empty after popping
  * we record at this point because after a pop if the ```stack``` is not empty then we are in a nesting.

## Code

```python
class Solution:
    def removeOuterParentheses(self, s: str) -> str:
        result = []
        stack = []
        for char in s:
            if char == '(':             # Encountered '(' - Opening
                if stack:               # non-empty stack -> detected nesting
                    result.append(char) # append '(' to result because this parenthesis is nested
                stack.append(char)      # append '(' to stack for each encounter
            else:                       # Encountered ')' - Closing
                stack.pop()             # pop last char from stack
                if stack:               # non-empty stack -> detected nesting
                    result.append(char) # append ')' to result because this parentheis closes the previous one and is nested
        return "".join(result)
```

## Time Complexity

<strong>O(n)</strong>, because each character is processed once

## Space Complexity

<strong>O(n)</strong>, because the stack recorcds '('

## Categories

<ul>
    <li>Array</li>
    <li>Strings</li>
    <li>Stack</li>
</ul>

[Back to Problem](../LC_1021_RemoveOutermostParentheses.md)