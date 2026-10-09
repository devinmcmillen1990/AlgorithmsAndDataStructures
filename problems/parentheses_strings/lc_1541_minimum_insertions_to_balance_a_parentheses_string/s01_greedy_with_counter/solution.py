class Solution:
    def minInsertions(self, s: str) -> int:
        insertions = 0              # tracks insertions made so far
        needed = 0                  # tracks the number of ')' needed
        for char in s:
            if char == '(':         # Encountered '(' - Opening
                if needed % 2 == 1: # we encountered a ')' before the current '(' -> {*()>}
                    insertions += 1 # need to insert a '('
                    needed -= 1     # (--) needed because we close the current set before starting another opening
                needed += 2         # new '(' requires 2 closing parentheses
            else:                   # Encountered ')' - Closing
                needed -= 1         # (--) needed because needed tracks the number of ')' required
                if needed < 0:      # there was no '(' available for the current ')'
                    insertions += 1 # insert '(' before the current ')'
                    needed = 1      # the insert above needs one more ')' to close
        return insertions + needed  # return (insertions made) + (number of needed ')')

'''
Example - ')('

Iteration 1 - ')'
    1. enter else block because char != '('
        a. (--)needed -> needed tracks number of ')' required, and since we have ')' we can decrement needed
        b. enter if block because needed < 0 [currently needed == -1]
            - (++)insertions -> we will need a '(' inserted for the current ')' [currently insertions == 1]
            - (++)needed -> we will need another ')' to close this set [currently needed == 1]

Iteration 2 - '('
    1. enter if block because char == '('
        a. enter if block because needed % 2 == 1 [Need to close the curret set ')' before tracking the '(']
            -- (++)insertions -> before we track the '(', we need to compute the remaining insertions for the previous set [')'] [currently insertions == 2]
            -- (--)needed -> stop tracking the previous set because we encountered a '(' [currently needed == 0]
        b. (+2)needed -> the new '(' requires '))' at this point [currently needed == 2]


Exit Loop

Return iterations + (2 * open_count) -> we know that we need 2 insertions for the first ')' and 2 more to close '(' 
    => 4 insertions

========================================================================================================================

Example - '()())'

Iteration 1 - '('
    1. enter if block because char == '('
        a. skip if block because needed % 2 != 1 [currently needed == 0]
        b. (+2) needed -> the new '(' required '))' [currently needed == 2]

Iteration 2 - ')'
    1. enter else block because char != '('
        a. (--)needed -> since needed tracks ')' and char == ')' we don't need another ')' [currently needed == 1]
        b. skip if block because needed > 0 [currently needed == 1]

Iteration 3 - '('
    1. enter if block because char == '('
        a. enter if block because needed % 2 == 1 [currently needed == 1]
            -- (++)insertions -> we know the previously tracked set needs an insertion to close [currently insertions == 1]
            -- (--)needed -> stop tracking the previous set because we encountered a '(' [currently needed == 0]
        b. (+2)needed -> the new '(' requires '))' at this point [currently needed == 2]

Iteration 4 - ')'
    1. enter else block because char != '('
        a. (--)needed -> since needed tracks ')' and char == ')' we don't need another ')' [currently needed == 1]
        b. skip if block because needed > 0 [currently needed == 1]

Iteration 5 - ')'
    1. enter else block because char != '('
        a. (--)needed -> since needed track ')' and char == ')' we don't need another ')' [currently needed == 0]
        b. skip if block because needed == 0 [currently needed == 0]

Exit Loop

Return insertions + (2 * open_count) because we know we need 1 insertion for the first '()' and none for the final '())'
    => 1 insertion
'''