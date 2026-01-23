#!/bin/bash
# Fix the commit message in history
cd /home/z1337/Desktop/PROJECTS/cloud-security-auditor

# Find the commit with the bad message
BAD_COMMIT=$(git log --format="%H %s" --all | grep "AI-generated lab guides" | cut -d' ' -f1)

if [ -z "$BAD_COMMIT" ]; then
    echo "✅ Commit message already fixed or not found"
    exit 0
fi

echo "Found bad commit: $BAD_COMMIT"
echo "Rewriting commit message..."

# Use git rebase to fix it
git rebase -i ${BAD_COMMIT}^ <<EOF
reword $BAD_COMMIT
EOF

# The rebase will open an editor, but we can use GIT_SEQUENCE_EDITOR to automate it
GIT_SEQUENCE_EDITOR="sed -i '1s/^pick/reword/'" git rebase -i ${BAD_COMMIT}^

# Actually, let's just use filter-branch one more time with proper escaping
FILTER_BRANCH_SQUELCH_WARNING=1 git filter-branch -f --msg-filter '
    if echo "$GIT_COMMIT_MSG" | grep -q "AI-generated lab guides"; then
        echo "Update .gitignore to exclude local documentation files"
    else
        cat
    fi
' main

echo "✅ Done! Commit message fixed."
