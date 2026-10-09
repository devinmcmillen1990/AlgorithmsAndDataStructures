<h1>3. Count Depth Contributions of Innermost Pairs</h2>

[Back to Problem](../LC_856_ScoreOfParentheses.md)

<h2>Idea</h2>

This solution removes the stack entirely. 

The key observation is:
<strong>Every contribution to th escore starts at an innermost () pair. Each closing pair doubles that contribution.</strong>

Examples
1. '()'         - Its innermost pair has 0 enclosing pairs -> 1
2. '(())'       - Its innermost pair has 1 enclosing pair  -> 2
3. '((()))'     - Its innermost pair has 2 enclosing pairs -> 4
4. '(((())))'   - Its innermost pair has 3 enclosing pairs -> 8

Therefore, contribution of an innermost pair = 2^(number of enclosing pairs)

When there are multiple innermost pairs, we add their contributions

<h2>Code</h2>

```python
class Solution:
    def scoreOfParentheses(self, s: str) -> int:
        score = 0
        depth = 0
        for i, char in enumerate(s):
            if char == '(':                 # Encounter '(' - Opening
                depth += 1                  # (++) depth on open parenthesis
            else:                           # Encounter ')' - Closing
                depth -= 1                  # (--) depth because we are closing
                if i > 0 and s[i-1] == '(': # if the previous char is '(' then we add to the score based on the depth
                    score += 1 << depth     # since its 2^(# of enclosing pairs) - Shift bits based on depth
        return score
```

<h2>Time Complexity : </h2> 

<strong>O(n)</strong>, because each character is processed once

<h2>Space Complexity : </h2> 

<strong>O(1)</strong>, no extra space required outside of the 2 integers

<h2>Categories</h2>

<ul>
    <li>Array</li>
    <li>Strings</li>
    <li>Bit Shift</li>
</ul>

[Back to Problem](../LC_856_ScoreOfParentheses.md)