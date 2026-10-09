class Solution:
    def removeOuterParentheses(self, s: str) -> str:
        result = []
        stack = []
        for char in s:
            if char == '(':
                if stack:
                    result.append(char)
                stack.append(char)
            else:
                stack.pop()
                if stack:
                    result.append(char)
        return "".join(result)