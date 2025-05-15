#!/bin/bash

LOG="jphaupt_phdthesis.log"

# First pass - get warning line numbers
echo "=== Finding warning locations ==="
grep -n "Warning" "$LOG" > warnings.tmp

# Second pass - extract context around warnings
echo "=== Warning details ==="
while IFS=: read -r line rest; do
    echo -e "\nWarning at line $line:"
    # Get 3 lines before and after each warning
    sed -n "$((line-3)),$((line+3))p" "$LOG"
done < warnings.tmp

# Cleanup
rm warnings.tmp

echo -e "\n=== Summary ==="
echo "Total warnings found: $(grep -c "Warning" "$LOG")"
