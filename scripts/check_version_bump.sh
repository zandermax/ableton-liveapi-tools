#!/usr/bin/env bash
# Ensures __version__ in ClaudeMCP_Remote/__init__.py is bumped before pushing to main.
set -euo pipefail

BRANCH=$(git symbolic-ref --short HEAD 2>/dev/null || echo "")

if [ "$BRANCH" != "main" ]; then
    exit 0
fi

VERSION_FILE="ClaudeMCP_Remote/__init__.py"
LOCAL_VERSION=$(grep -E '^__version__' "$VERSION_FILE" | head -1)

# Fetch silently so we have an up-to-date ref without printing noise
git fetch origin main --quiet 2>/dev/null || true

if ! git rev-parse origin/main >/dev/null 2>&1; then
    # No remote main yet (first push), allow it
    exit 0
fi

REMOTE_VERSION=$(git show origin/main:"$VERSION_FILE" | grep -E '^__version__' | head -1)

if [ "$LOCAL_VERSION" = "$REMOTE_VERSION" ]; then
    echo ""
    echo "ERROR: __version__ in $VERSION_FILE has not been bumped."
    echo "  Remote: $REMOTE_VERSION"
    echo "  Local:  $LOCAL_VERSION"
    echo ""
    echo "Update __version__ before pushing to main."
    echo ""
    exit 1
fi

echo "Version bump detected: $REMOTE_VERSION -> $LOCAL_VERSION"
exit 0
