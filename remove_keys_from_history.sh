#!/bin/bash
# Script to remove API keys from git history
cd /home/z1337/Desktop/PROJECTS/cloud-security-auditor

# Create a backup branch first
git branch backup-before-key-removal

# Use git filter-repo if available, otherwise use filter-branch
if command -v git-filter-repo &> /dev/null; then
    echo "Using git-filter-repo..."
    git filter-repo --invert-paths --path API_KEYS_REFERENCE.md --path LAB_EXECUTION_GUIDE.md --force
else
    echo "Using git filter-branch (slower)..."
    FILTER_BRANCH_SQUELCH_WARNING=1 git filter-branch --force --index-filter '
        if git ls-files --error-unmatch API_KEYS_REFERENCE.md >/dev/null 2>&1; then
            git rm --cached --ignore-unmatch API_KEYS_REFERENCE.md
        fi
        if git ls-files --error-unmatch LAB_EXECUTION_GUIDE.md >/dev/null 2>&1; then
            git rm --cached --ignore-unmatch LAB_EXECUTION_GUIDE.md
        fi
    ' --prune-empty --tag-name-filter cat -- main
fi

echo "Done! Keys removed from git history."
echo "To restore if needed: git reset --hard backup-before-key-removal"
