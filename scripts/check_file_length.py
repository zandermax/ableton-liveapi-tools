#!/usr/bin/env python3
"""Pre-commit hook: fail if any Python file exceeds MAX_LINES lines."""

import sys

MAX_LINES = 300

failures = []
for path in sys.argv[1:]:
    try:
        with open(path, encoding="utf-8") as f:
            count = sum(1 for _ in f)
        if count > MAX_LINES:
            failures.append((path, count))
    except OSError as exc:
        print(f"error reading {path}: {exc}", file=sys.stderr)
        sys.exit(1)

for path, count in failures:
    print(f"{path}: {count} lines (max {MAX_LINES})")

sys.exit(1 if failures else 0)
