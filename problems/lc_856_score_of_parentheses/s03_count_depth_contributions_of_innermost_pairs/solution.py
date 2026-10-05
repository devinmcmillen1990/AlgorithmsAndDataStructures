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