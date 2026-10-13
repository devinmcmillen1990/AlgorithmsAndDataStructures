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

'''
Example - '(())()'

Iteration 1 - '('
    1. enter if block because char == '('
        a. skip if block because stack is empty [currently stack == []]
        b. append '(' to stack [currently stack == ['('] ]

Iteration 2 - '('
    1. enter if block because char == '('
        a. enter if block because stack is NOT empty [currently stack == ['('] ]
            -- append '(' to result because this is in a nesting [currently result == ['('] ]
        b. append '(' to stack [currently stack == ['(', '('] ]

Iteration 3 - ')'
    1. enter else block because char != '('
        a. pop from stack [currently stack == ['('] ]
        b. enter if block because stack is not empty (nesting detected)
            -- append ')' to result because this is in a nesting [currently result == ['(', ')'] ]

Iteration 4 - ')'
    1. enter else block because char != '('
        a. pop from stack [currently stack == [] ]
        b. skip if block because stack is empty -> outer parentheses pair detected so don't record

Iteration 5 - '('
    1. enter if block because char == '('
        a. skip if block because stack is empty [currently stack == [] ]
        b. append '(' to stack [currently stack == ['(']]

Iteration 6 - ')'
    1. enter else block because char != '('
        a. pop from stack [currently stack == [] ]
        b. skip if block because stack is empty [currently stack == [] ]

Exit Loop

Return result ['()']

========================================================================================================================

Example - '(()())(())'

Iteration 1 = '('
    1. enter if block because char == '('
        a. skip if block because stack is empty [currently stack = [] ]
        b. append '(' to stack [currently stack == ['('] ]

Iteration 2 - '('
    1. enter if block because char == '('
        a. enter if block because stack is not empty [currently stack == ['('] ]
            -- append '(' to result because this is in a nesting [currently result = ['('] ]
        b. append '(' to stack [currently stack == ['(', '('] ]

Iteration 3 - ')'
    1. enter else block because char != '('
        a. pop from stack [currently stack == ['('] ]
        b. enter if block because stack is not empty
            -- append ')' to result because this is in a nesting [currently result == ['(', ')'] ]

Iteration 4 - '('
    1. enter the if block because char == '('
        a. enter if block because stack is not empty -> we are in a nesting
            -- append '(' to result because we are in a nesting [currently result = ['(', ')', '('] ]
        b. append '(' to stack [currently stack == ['(', '('] ]

Iteration 5 - ')' 
    1. enter else block because char != '('
        a. pop from stack [currently stack = ['('] ]
        b. enter if block because stack is not empty
            -- append ')' to result because this is in a nesting [currently result == ['(', ')', '(', ')'] ]

Iteration 6 - ')'
    1. enter else block because char != '('
        a. pop from stack [currently stack = [] ]
        b. skip if block because stack is empty [currently stack == [] ]

Iteration 7 - '('
    1. enter if block because char == '('
        a. skip if block because stack is empty [currently stack = [] ]
        b. append '(' to stack [currently stack == ['('] ]

Iteration 8 - '('
    1. enter if block because char == '('
        a. enter if block because stack is not empty [currently stack == ['('] ]
            -- append '(' to result because we are in a nesting [currently result == ['(', ')', '(', ')', '('] ]
        b. append '(' to stack [currently stack == ['(', '('] ]

Iteration 9 - ')'
    1. enter else block because char != '('
        a. pop from stack [currently stack == ['('] ]
        b. enter if block because stack is not empty
            -- append ')' to result because we are in a nesting [currently result == ['(', ')', '(', ')', '(', ')'] ]

Exit Loop

Return result ['()()()']

'''