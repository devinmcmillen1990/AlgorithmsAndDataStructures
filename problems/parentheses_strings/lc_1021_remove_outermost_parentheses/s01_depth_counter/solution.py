class Solution:
    def removeOuterParentheses(self, s: str) -> str:
        result = []
        depth = 0                       # Used to track how many parentheses are currently unmatched
        for char in s:
            if char == '(':             # Encountered '(' - Opening
                if depth > 0:           # check depth before (++) depth. means we have already seen a '('
                    result.append(char) # append '(' because this parenthesis is nested because depth > 0
                depth += 1              # (++) depth each iteration we encounter '('
            else:                       # Encounter ')' - Closing
                depth -= 1              # (--) depth each iteration we encounter ')'
                if depth > 0:           # check depth after incrementing. if depth is 0 then this ')' closes the final parenthesis
                    result.append(char) # append ')' to the output result
        return "".join(result)


'''
Example - '(())()'

Iteration 1 - '('
    1. enter if block because char == '('
        a. skip if block because depth == 0 [currently depth == 0]
        b. (++)depth -> depth tracks '(' to find nested parentheses [currently depth == 1]

Iteration 2 - '('
    1. enter if block because char == '('
        a. enter if block because depth > 0 [currently depth == 1]
            -- append char to result [currently result == '(']
        b. (++)depth -> depth tracks '(' to find nested parentheses [currently depth == 2]

Iteration 3 - ')'
    1. enter else block because char == ')'
        a. (--)depth -> we have a ')' so this pair is closed [currently depth == 1]
        b. enter if block because depth > 0 [currently depth == 1]
            -- append char to result [currently result == '()']

Iteration 4 - ')'
    1. enter else block because char != '('
        a. (--)depth -> we have a ')' so this pair is closed [currently depth == 0]
        b. skip if block because depth == 0 [currently depth == 0]

Iteration 5 - '('
    1. enter if block because char == '('
        a. skip if block because depth == 0 [currently depth == 0]
        b. (++)depth -> depth tracks '(' to find nested parentheses [currently depth == 1]

Iteration 6 - ')'
    1. enter else block because char != '('
        a. (--)depth -> we have a ')' so this pair is closed [currently depth == 0]
        b. skip if block because depth == 0 [currently depth == 0]

Exit Loop

Return result ['()']

========================================================================================================================

Example - '(()())(())'

Iteration 1 - '('
    1. enter if block because char == '('
        a. skip if block because depth == 0 [currently depth == 0]
        b. (++)depth -> depth tracks '(' to find nested parentheses [currently depth == 1]

Iteration 2 - '('
    1. enter if block because char == '('
        a. enter if block because depth > 0 [currently depth == 1]
            -- append char to result [result == '(']
        b. (++)depth -> depth tracks '(' to find nested parentheses [currently depth == 2]

Iteration 3 - ')'
    1. enter else block because char !- ')'
        a. (--)depth -> we have a ')' so this pair is closed [currently depth == 1]
        b. enter if block because depth > 0 [currently depth == 1]
            -- append char to result [result == '()']

Iteration 4 - '('
    1. enter if block because char == '('
        a. enter if block because depth > 0 [currently depth == 1]
            -- append char to result [result == '()(']
        b. (++)depth -> depth tracks '(' to find nested parentheses [currently depth == 2]

Iteration 5 - ')'
    1. enter else block because char != '('
        a. (--)depth -> we have a ')' so this pair is closed [currently depth == 1]
        b. enter if block because depth > 0 [currently depth == 1]
            -- append char to result [result == '()()']

Iteration 6 - ')'
    1. enter else block because char != '('
        a. (--)depth -> we have a ')' so this pair is closed [currently depth == 0]
        b. skip if block because depth == 0 [currently depth == 0]
    
Iteration 7 - '('
    1. enter if block because char == '('
        a. skip if block because depth == 0 [currently depth == 0]
        b. (++)depth -> depth tracks '(' to find nested parentheses [currently depth == 1]

Iteration 8 - '('
    1. enter if block because char == '('
        a. enter if block because depth > 0 [currently depth == 1]
            -- append char to result [currently result == '()()(']
        b. (++)depth -> depth tracks '(' to find nested parentheses [currently depth == 2]

Iteration 9 - ')'
    1. enter else block because char != '('
        a. (--)depth -> we have a ')' so this pair is closed [currently depth == 1]
        b. enter if block because depth > 0 [currently depth == 1]
            -- append char to result [currently result = '()()()']

Iteration 10 - ')'
    1. enter else block because char != '('
        a. (--)depth -> we have a ')' so this pair is closed [currently depth == 0]
        b. skip else block because depth == 0 [currently depth == 0]

Exit Loop

Return result ['()()()']

'''