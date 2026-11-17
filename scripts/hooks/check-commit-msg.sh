#!/usr/bin/env bash
MSG_FILE="$1"
MSG=$(head -1 "$MSG_FILE")

if echo "$MSG" | grep -qE "^(Merge|Revert) "; then
    exit 0
fi

if echo "$MSG" | grep -qE "^#[0-9]+ (feat|fix|docs|test|refactor|chore|ci|perf|style)\([a-z0-9-]+\): .+$"; then
    exit 0
fi

echo "❌ Invalid commit message format."
echo "    Expected: #<issue> <type>(<scope>): <description>"
echo "    Example:  #1 feat(auth): add login endpoint"
exit 1
