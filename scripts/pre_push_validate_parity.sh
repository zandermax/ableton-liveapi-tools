#!/usr/bin/env bash
set -euo pipefail

# Pre-push parity validation hook
# Runs registry parity; optionally runs wiki->site parity when generated target exists.

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

echo "Running registry ↔ code ↔ wiki parity check..."
python3 scripts/validate_registry_parity.py --check || {
  echo "Registry parity validation failed. Abort push." >&2
  exit 1
}

TARGET_DIR="_Node/webui"
if [ -d "$TARGET_DIR" ]; then
  echo "Running wiki -> generated-site parity check against $TARGET_DIR..."
  ARTIFACTS_DIR="$REPO_ROOT/tmp/parity_artifacts/$(date -u +"%Y%m%dT%H%M%SZ")"
  mkdir -p "$ARTIFACTS_DIR"
  python3 scripts/validate_wiki_parity.py --check --source docs/wiki --target "$TARGET_DIR" --json --fail-on-mismatch --artifacts-dir "$ARTIFACTS_DIR" || {
    echo "Wiki parity validation failed. See artifacts: $ARTIFACTS_DIR" >&2
    exit 1
  }
else
  echo "Target $TARGET_DIR not found; skipping wiki->site parity check. To enable, build site locally."
fi

echo "Parity checks passed. Continuing push."
exit 0
