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