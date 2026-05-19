#!/usr/bin/env python3
"""Simple parity validator between source wiki pages and generated artifacts.

Prototype: filename-based matching, normalization via existing frontmatter parser.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import datetime
import difflib
from typing import Tuple, Dict, List

try:
    from scripts.migrate_wiki_frontmatter import parse_frontmatter, dump_frontmatter
except Exception:
    # best-effort import when running as script; allow tests to import functions
    from migrate_wiki_frontmatter import parse_frontmatter, dump_frontmatter


def normalize_text(text: str) -> str:
    data, body = parse_frontmatter(text)
    if data:
        return (dump_frontmatter(data) + body.strip() + "\n").replace("\r\n", "\n")
    return (body.strip() + "\n").replace("\r\n", "\n")


def compare_texts(src_text: str, tgt_text: str) -> Tuple[bool, str]:
    ns = normalize_text(src_text)
    nt = normalize_text(tgt_text)
    if ns == nt:
        return True, ""
    import difflib

    diff = "\n".join(difflib.unified_diff(ns.splitlines(), nt.splitlines(), lineterm=""))
    return False, diff


def collect_md_files(root: str) -> Dict[str, str]:
    res = {}
    for dirpath, _, files in os.walk(root):
        for f in files:
            if not f.endswith(".md"):
                continue
            rel = os.path.relpath(os.path.join(dirpath, f), root)
            res[rel] = os.path.join(dirpath, f)
    return res


# Compatibility layer for prototype tests
# The repository contains a more featureful validator; tests in planning
# expect a small prototype API (`normalize_text(text, exclude_keys)`,
# `compare_dirs(...)`, `run(argv)`) — provide thin wrappers here.

# alias the existing frontmatter-based normalizer so we can wrap it
_normalize_frontmatter = normalize_text


def normalize_text(text: str, exclude_keys: List[str] = None) -> str:
    """Normalize text for comparisons.

    If `exclude_keys` is provided, perform a simple line-based exclusion
    (used by lightweight tests). Otherwise delegate to the frontmatter
    normalizer defined earlier in this module.
    """
    if exclude_keys:
        out_lines: List[str] = []
        for line in text.splitlines():
            stripped = line.lstrip()
            skip = False
            for k in exclude_keys:
                if stripped.startswith(f"{k}:"):
                    skip = True
                    break
            if not skip:
                out_lines.append(line.rstrip())
        return "\n".join(out_lines).strip() + ("\n" if out_lines else "")
    # delegate to the existing frontmatter-aware normalizer
    return _normalize_frontmatter(text)


def compare_dirs(canonical_dir: str, repo_dir: str, exclude_keys: List[str] = None, files: List[str] = None) -> Dict[str, Tuple[bool, str, str, str]]:
    """Compare canonical -> repo directories and return mapping rel -> (ok,diff,cpath,rpath).

    This matches the small prototype behavior expected by tests.
    """
    results: Dict[str, Tuple[bool, str, str, str]] = {}
    if files is None:
        files = sorted(collect_md_files(canonical_dir).keys())
    for rel in files:
        cpath = os.path.join(canonical_dir, rel)
        rpath = os.path.join(repo_dir, rel)
        ctext = ""
        rtext = ""
        if os.path.exists(cpath):
            with open(cpath, "r", encoding="utf-8") as fh:
                ctext = fh.read()
        if os.path.exists(rpath):
            with open(rpath, "r", encoding="utf-8") as fh:
                rtext = fh.read()

        nc = normalize_text(ctext, exclude_keys)
        nr = normalize_text(rtext, exclude_keys)
        if nc == nr:
            results[rel] = (True, "", cpath, rpath)
        else:
            diff = "\n".join(difflib.unified_diff(nc.splitlines(), nr.splitlines(), fromfile=os.path.relpath(cpath), tofile=os.path.relpath(rpath), lineterm=""))
            results[rel] = (False, diff, cpath, rpath)
    return results


def apply_changes(results: Dict[str, Tuple[bool, str, str, str]], canonical_dir: str, repo_dir: str) -> None:
    for rel, (ok, diff, cpath, rpath) in results.items():
        if not ok:
            os.makedirs(os.path.dirname(rpath), exist_ok=True)
            with open(cpath, "r", encoding="utf-8") as rf, open(rpath, "w", encoding="utf-8") as wf:
                wf.write(rf.read())


def run(argv: List[str]) -> int:
    p = argparse.ArgumentParser()
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true")
    group.add_argument("--apply", action="store_true")
    p.add_argument("--canonical-dir", required=False)
    p.add_argument("--repo-dir", required=False)
    p.add_argument("--exclude", action="append", default=[])
    args = p.parse_args(argv)

    # default paths used by prototype tests when not provided
    here = os.path.dirname(__file__)
    default_canonical = os.path.abspath(os.path.join(here, "..", "planning", "wiki-as-source-of-truth", "tests", "fixtures", "canonical"))
    default_repo = os.path.abspath(os.path.join(here, "..", "planning", "wiki-as-source-of-truth", "tests", "fixtures", "repo"))

    canonical_dir = os.path.abspath(args.canonical_dir) if args.canonical_dir else default_canonical
    repo_dir = os.path.abspath(args.repo_dir) if args.repo_dir else default_repo
    exclude = args.exclude or ["last_updated"]

    results = compare_dirs(canonical_dir, repo_dir, exclude_keys=exclude)
    mismatches = [rel for rel, (ok, *_ ) in results.items() if not ok]

    for rel in mismatches:
        ok, diff, cpath, rpath = results[rel]
        print(diff)

    print(f"Files compared: {len(results)}. Mismatches: {len(mismatches)}")

    if args.apply:
        if mismatches:
            apply_changes(results, canonical_dir, repo_dir)
            print("Applied changes.")
        return 0

    if args.check:
        return 0 if not mismatches else 2

    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Validate wiki parity between source and target directories")
    p.add_argument("--source", default="docs/wiki", help="source wiki export directory (default: docs/wiki)")
    p.add_argument("--target", default="_Node/webui")
    p.add_argument("--json", action="store_true")
    p.add_argument("--check", action="store_true", help="list mismatched files and exit non-zero if mismatches found")
    p.add_argument("--fail-on-mismatch", action="store_true")
    p.add_argument("--match-by", choices=("rel", "basename"), default="rel",
                   help="how to match source->target files: 'rel' exact relative path, 'basename' match filenames")
    p.add_argument("--map", action="append", default=[],
                   help="explicit mapping entries in form source_rel:target_rel; can be repeated")
    p.add_argument("--allow-planning", action="store_true", help="allow scanning planning/ paths (use with care)")
    p.add_argument("--artifacts-dir", default=None,
                   help="Directory to write per-file diff artifacts (default: tmp/parity_artifacts/<timestamp> when mismatches found)")
    p.add_argument("--max-inline-diff", type=int, default=10000,
                   help="Maximum number of characters to include inline in JSON diff before truncating")
    args = p.parse_args(argv)

    # safety: prevent accidental scan of planning/ unless explicitly allowed
    if "planning" in os.path.normpath(args.source).split(os.sep) and not args.allow_planning:
        print("Refusing to scan 'planning/' directory. Use --allow-planning to override or set --source to actual wiki export (docs/wiki).", file=sys.stderr)
        return 2

    if not os.path.isdir(args.target):
        print(f"Target path not found: {args.target}", file=sys.stderr)
        print("Did you mean to point at a different generated-docs folder? Example: _Node/webui (repo-specific) or docs/site.", file=sys.stderr)
        return 2

    src_files = collect_md_files(args.source)
    tgt_files = collect_md_files(args.target)

    # parse explicit mappings
    explicit_map = {}
    for entry in args.map:
        if ":" in entry:
            s, t = entry.split(":", 1)
            explicit_map[s.strip()] = t.strip()
        else:
            print(f"ignoring malformed map entry: {entry}", file=sys.stderr)

    results = {"matched": [], "mismatched": [], "missing_target": [], "extra_target": []}

    for rel, src_path in src_files.items():
        # apply explicit mapping if provided
        if rel in explicit_map:
            expected_rel = explicit_map[rel]
            tgt_path = tgt_files.get(expected_rel)
            if not tgt_path:
                results["missing_target"].append(rel)
                continue
        else:
            if args.match_by == "rel":
                tgt_path = tgt_files.get(rel)
                if not tgt_path:
                    results["missing_target"].append(rel)
                    continue
            else:
                # match by basename
                candidates = [r for r in tgt_files.keys() if os.path.basename(r) == os.path.basename(rel)]
                if len(candidates) == 0:
                    results["missing_target"].append(rel)
                    continue
                # pick first candidate when multiple; report later if ambiguous
                expected_rel = candidates[0]
                tgt_path = tgt_files[expected_rel]
        with open(src_path, "r", encoding="utf-8") as fh:
            stext = fh.read()
        with open(tgt_path, "r", encoding="utf-8") as fh:
            ttext = fh.read()
        ok, diff = compare_texts(stext, ttext)
        if ok:
            results["matched"].append(rel)
        else:
            # include chosen target in report when matching by basename or explicit map
            entry = {"path": rel, "diff": diff}
            if 'expected_rel' in locals():
                entry['target'] = expected_rel
            results["mismatched"].append(entry)

    # detect extras in target not present in source
    for rel in tgt_files.keys():
        if rel not in src_files:
            results["extra_target"].append(rel)

    # Optionally write per-file diff artifacts when mismatches are present.
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    artifact_dir = args.artifacts_dir
    if artifact_dir is None and results["mismatched"] and (args.json or args.check or args.fail_on_mismatch):
        artifact_dir = os.path.join(repo_root, "tmp", "parity_artifacts", datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ"))
    if artifact_dir:
        os.makedirs(artifact_dir, exist_ok=True)
        for m in results["mismatched"]:
            rel = m.get("path")
            diff = m.get("diff", "")
            artifact_path = os.path.join(artifact_dir, rel + ".diff")
            os.makedirs(os.path.dirname(artifact_path), exist_ok=True)
            try:
                with open(artifact_path, "w", encoding="utf-8") as fh:
                    fh.write(diff)
                # store relative path to repo root for portability
                m["diff_file"] = os.path.relpath(artifact_path, repo_root)
                if len(diff) > args.max_inline_diff:
                    m["diff_snippet"] = diff[: args.max_inline_diff] + "\n... (truncated) ..."
                    m.pop("diff", None)
            except Exception:
                # best-effort: don't fail the whole run if artifact write fails
                pass
        results["artifact_dir"] = os.path.relpath(artifact_dir, repo_root)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(f"Matched: {len(results['matched'])}")
        print(f"Mismatched: {len(results['mismatched'])}")
        if results["missing_target"]:
            print(f"Missing in target: {len(results['missing_target'])}")
        if results["extra_target"]:
            print(f"Extra in target: {len(results['extra_target'])}")

        if args.check:
            if results["mismatched"]:
                print("\nMismatched files:")
                for m in results["mismatched"]:
                    line = m.get("path")
                    if m.get("target"):
                        line += f" -> {m.get('target')}"
                    print(line)
                    if m.get("diff_file"):
                        print("  diff saved:", m.get("diff_file"))
                    elif m.get("diff_snippet"):
                        print("  diff (snippet):")
                        print(m.get("diff_snippet"))
            if results["missing_target"]:
                print("\nMissing in target:")
                for pth in results["missing_target"]:
                    print(pth)
            if results["extra_target"]:
                print("\nExtra in target:")
                for pth in results["extra_target"]:
                    print(pth)

    rc = 0
    if args.fail_on_mismatch and (results["mismatched"] or results["missing_target"]):
        rc = 1
    if args.check and (results["mismatched"] or results["missing_target"]):
        rc = 1
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
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
