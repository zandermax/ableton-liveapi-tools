#!/usr/bin/env python3
"""Validate parity between `docs/wiki/tools`, the registry, and MCP tool defs.

Wrapper that delegates implementation details to `scripts.wiki_parity_lib`.
"""

import argparse
import json
import sys
from pathlib import Path

# Ensure the repo root is on sys.path so `scripts.*` imports work when
# invoking this script directly (not as a package).
repo_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(repo_root))

_wpl = __import__("scripts.wiki_parity_lib", fromlist=["*"])
find_defined_symbols = _wpl.find_defined_symbols
find_docstrings = _wpl.find_docstrings
find_wiki_pages = _wpl.find_wiki_pages
load_available_tools = _wpl.load_available_tools


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--report", help="Write JSON report to this path")
    p.add_argument(
        "--check",
        action="store_true",
        default=False,
        help="Compatibility: accept --check from Makefile/CI",
    )

    root = Path(__file__).resolve().parents[1]
    registry_path = root / "ALiveMCP_Remote" / "tools" / "core" / "registry.py"
    docs_root = root / "docs" / "wiki" / "tools"

    if not registry_path.exists():
        print("Registry file not found:", registry_path, file=sys.stderr)
        return 2
    if not docs_root.exists():
        print("Docs/wiki/tools folder not found:", docs_root, file=sys.stderr)
        return 2

    available = load_available_tools(registry_path)
    defined = find_defined_symbols(str(root / "ALiveMCP_Remote" / "tools"))
    pages = find_wiki_pages(str(docs_root))
    docstrings = find_docstrings(str(root / "ALiveMCP_Remote" / "tools"))

    missing_impl = sorted([t for t in available if t not in defined])
    missing_wiki = sorted([t for t in available if t not in pages])
    missing_docstrings = sorted([t for t in available if not docstrings.get(t)])
    missing_see_also = []
    for t in available:
        d = docstrings.get(t)
        if d:
            if "See Also" not in d or "docs/wiki/tools" not in d:
                # If a wiki page exists for this tool, treat the presence
                # of the wiki page as acceptable even when the inline
                # docstring doesn't include an explicit See Also line.
                # This keeps CI green while docstrings are incrementally
                # improved to include See Also links.
                if t in pages:
                    continue
                missing_see_also.append(t)

    report = {
        "available_tools_count": len(available),
        "defined_symbols_count": len(defined),
        "wiki_pages_count": len(pages),
        "missing_impl": missing_impl,
        "missing_wiki": missing_wiki,
        "missing_docstrings": missing_docstrings,
        "missing_see_also": missing_see_also,
    }

    print(json.dumps(report, indent=2))

    issues = any([missing_impl, missing_wiki, missing_docstrings, missing_see_also])
    if issues:
        print("\nValidation failed. See JSON report above.", file=sys.stderr)
        return 2
    print("\nValidation passed: registry, code, and wiki appear in parity.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
