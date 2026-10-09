class Solution:
    def minInsertions(self, s: str) -> int:
        insertions = 0                                  # tracks insertions made so far
        open_count = 0                                  # tracks # of unmatched ')'
        i = 0                                           
        while i < len(s):
            if s[i] == '(':                             # Encountered '(' - Opening
                open_count += 1                         # (++) open_count
                i += 1                                  # (++) i
            else:                                       # Encountered ')' - Closing
                if i + 1 < len(s) and s[i + 1] == ')':  # Check if next char forms '))'
                    i += 2                              # (i+=2), closing set already exists
                else:                                   # following char is actually a '(', so only 1 ')' exists
                    insertions += 1                     # (++) insertions, since we have only 1 ')' insert its partner
                    i += 1                              
                if open_count > 0:                      # match the closing pair with an opening since we encountered ')'
                    open_count -= 1
                else:                                   # match not found
                    insertions += 1                     # (++) insertions, requires insert a '(' before this closing pair
        return insertions + 2 * open_count

'''
Example - ')('

Iteration 1 - ')'
    1. enter else block because s[i] != '('
        a. enter else block because s[i+1] != ')'
            -- (++)insertions -> we need 1 ')' if we have open_count > 0 and an extra '(' if open_count == 0
        b. enter else block because open_count == 0
            -- (++)insertions -> since open_count == 0 we also need '(' to be inserted 
                * [insertions == 2 at this point]

Iteration 2 - '('
    1. enter if block because s[i] == '('
        a. (++)open_count -> this will require 2 insertions if it is not closed with proceeding '))'

Exit Loop

Return iterations + (2 * open_count) -> we know that we need 2 insertions for the first ')' and 2 more to close '(' 
    => 4 insertions

========================================================================================================================

Example - '()())'

Iteration 1 - '('
    1. enter if block because s[i] == '('
        -- (++)open_count -> this will require 2 insertions if it is not closed with proceeding '))'
            * [open_count == 1 at this point]

Iteration 2 - ')'
    1. enter else block because s[i] != '('
        a. enter else block because s[i+1] != ')'
            (++)insertions -> we need 1 ')' if we have open_count > 0 and an extra '(' if open_count == 0
                * [insertions == 1 at this point]
        b. enter if block because open_count > 0 [currently open_count == 1]
            (--)open_count because we counted the insertion that we will need to close '()' above
                * [open_count == 0 at this point]

Iteration 3 - '('
    1. enter if block because s[i] == '('
            -- (++)open_count -> this will require 2 insertions if it is not closed with proceeding '))'
                * [open_count == 1 at this point]

Iteration 4 - ')'
    1. enter else block because s[i] != '('
        a. enter if block because s[i+1] == ')'
            -- closing pair found so move variable <i> past the following index and no insertions needed
        b. enter if block because open_count > 0 [currently open_count == 1]
            (--)open_count because we closed this pair and no insertions are needed

Iteration 5 - Skipped because the last iteration closed the pair
    
Exit Loop

Return insertions + (2 * open_count) because we know we need 1 insertion for the first '()' and none for the final '())'
    => 1 insertion
'''