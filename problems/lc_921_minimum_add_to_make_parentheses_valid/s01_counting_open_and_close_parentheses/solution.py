class Solution:
    def minAddToMakeValid(self, s: str) -> int:
        unmatched_open, missing_open = 0, 0
        for char in s:
            if char == '(':             # Encounter '(' - Opening
                unmatched_open += 1     # (++) unmatched_open
            elif unmatched_open > 0:    # Encounter ')' - Closing AND we tracked some unmatched ')'
                unmatched_open -= 1     # (--) unmatched_open because we have a ')' for the tracked unmatched '('
            else:                       # Encounter ')' - Closing AND we have no unmatched ')'
                missing_open += 1       # (++) missing_open because this means that we have a '(' and don't have an unmatched ')'.
        return missing_open + unmatched_open