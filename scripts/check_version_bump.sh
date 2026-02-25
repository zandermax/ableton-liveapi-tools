#!/usr/bin/env bash
# Ensures __version__ in ALiveMCP_Remote/__init__.py is bumped before pushing to main.
set -euo pipefail

BRANCH=$(git symbolic-ref --short HEAD 2>/dev/null || echo "")

if [ "$BRANCH" != "main" ]; then
    exit 0
fi

VERSION_FILE="ALiveMCP_Remote/__init__.py"
LOCAL_VERSION=$(grep -E '^__version__' "$VERSION_FILE" | head -1)

# Fetch silently so we have an up-to-date ref without printing noise
git fetch origin main --quiet 2>/dev/null || true

if ! git rev-parse origin/main >/dev/null 2>&1; then
    # No remote main yet (first push), allow it
    exit 0
fi

# Check if the file even exists in origin/main (it may be a newly added file)
if ! git cat-file -e "origin/main:$VERSION_FILE" 2>/dev/null; then
    echo "$VERSION_FILE is new (not in origin/main) — skipping version check."
    exit 0
fi

# Temporarily disable exit-on-error so we can capture and report git show failures
set +e
REMOTE_SHOW=$(git show "origin/main:$VERSION_FILE" 2>&1)
SHOW_EXIT=$?
set -e
if [ $SHOW_EXIT -ne 0 ]; then
    echo ""
    echo "ERROR: Could not read $VERSION_FILE from origin/main:"
    echo "  $REMOTE_SHOW"
    echo ""
    exit 1
fi

REMOTE_VERSION=$(echo "$REMOTE_SHOW" | grep -E '^__version__' | head -1)

if [ -z "$REMOTE_VERSION" ]; then
    echo ""
    echo "ERROR: Could not find __version__ in origin/main:$VERSION_FILE"
    echo ""
    exit 1
fi

if [ "$LOCAL_VERSION" = "$REMOTE_VERSION" ]; then
    echo ""
    echo "ERROR: __version__ in $VERSION_FILE has not been bumped."
    echo "  Remote (origin/main): $REMOTE_VERSION"
    echo "  Local  (this branch): $LOCAL_VERSION"
    echo ""
    echo "Bump __version__ in $VERSION_FILE before pushing to main."
    echo ""
    exit 1
fi

echo "Version bump OK: $REMOTE_VERSION -> $LOCAL_VERSION"
exit 0
