<h1>2. Recurse, Letting each Recursive Call Evaluate One Level</h2>

[Back to Problem](../LC_856_ScoreOfParentheses.md)

<h2>Idea</h2>

This follows the same idea as the stack but uses nested function calls instead of an explicit stack.

We will need a helper function that will add up groups at its current level, stopping when it reaches a closing parenthesis or the end of the string.

Whenever it sees '(', it class itself to evaluate the contents.

<h2>Code</h2>

'''python
class Solution:
    def scoreOfParentheses(self, s: str) -> int:
        index = 0
        def parse() -> int:                             # helper function for recursion
            nonlocal index                              # this allows the parse() function to modify the index in the parent function
            total = 0
            while index < len(s) and s[index] == '(':   # parse all the '(' at this recursion level
                index += 1                              # (++) index because we have '('
                inner = parse()                         # with index (++), recurse until we hit the end of the nesting.
                index += 1                              # (++) index after the parse() call to move the pointer
                if inner == 0:                          # only found '()'
                    total += 1                      
                else:                                   # found nested parentheses
                    total += 2 * inner
            return total                                # return recursive iteration's total.
        return parse()
'''

<h2>Time Complexity : </h2> 

<strong>O(n)</strong>, because the shared index only moves forward

<h2>Space Complexity : </h2> 

<strong>O(h)</strong>, where 'h' is the maximum nesting depth (recursive call depth)

<h2>Categories</h2>

<ul>
    <li>Array</li>
    <li>Strings</li>
    <li>Recursion</li>
</ul>