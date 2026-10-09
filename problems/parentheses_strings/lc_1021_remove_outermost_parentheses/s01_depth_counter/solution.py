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