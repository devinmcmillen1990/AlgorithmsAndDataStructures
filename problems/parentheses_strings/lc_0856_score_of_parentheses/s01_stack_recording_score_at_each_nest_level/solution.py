class Solution:
    def scoreOfParentheses(self, s: str) -> int:
        stack = [0]                         # Set first entry to '0'. This will track the score of the whole expression
        for char in s:
            if char == '(':                 # Encounter '(' - Opening
                stack.append(0)             # start a new group with the innermost score '0'
            else:                           # Encounter ')' - Closing
                inner = stack.pop()         # get the score inside the group we are closing
                if inner == 0:              # nothing inside means this group is '()'
                    group_score = 1         
                else:
                    group_score = 2 * inner # wrapping nonempty group to its parent's score
                stack[-1] += group_score    # add this completed group to its parent's score
        return stack[0]