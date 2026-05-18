#!/usr/bin/env python3
"""Migrate wiki frontmatter.

Idempotent, safe, provides --check and --apply modes. Lightweight YAML
fallback implemented for environments without PyYAML.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import datetime, date
from typing import Any, Dict, Tuple

try:
    import yaml
except Exception:
    yaml = None


def parse_frontmatter(text: str) -> Tuple[Dict[str, Any], str]:
    """Return (frontmatter_dict, body).

    Supports full PyYAML when available. Falls back to small subset parser
    that understands simple key: value and block lists (`- item`).
    """
    if not text.startswith("---"):
        return {}, text

    markers = list(re.finditer(r"^---\s*$", text, flags=re.MULTILINE))
    if len(markers) < 2:
        return {}, text

    start = markers[0].end()
    end = markers[1].start()
    fm_raw = text[start:end].strip("\n")
    body = text[markers[1].end():]

    if yaml:
        data = yaml.safe_load(fm_raw) or {}
        return data, body

    def parse_scalar(s: str) -> Any:
        s_str = s.strip()
        sl = s_str.lower()
        if sl in ("yes", "y", "true", "t"):
            return True
        if sl in ("no", "n", "false", "f"):
            return False
        # ints
        if re.fullmatch(r"[+-]?\d+", s_str):
            try:
                return int(s_str)
            except Exception:
                pass
        # floats
        if re.fullmatch(r"[+-]?\d+\.\d+", s_str):
            try:
                return float(s_str)
            except Exception:
                pass
        return s_str

    # Fallback parser: handles `key: value`, `key:`, then indented `- item` lines,
    # and inline comma-separated lists.
    data: Dict[str, Any] = {}
    lines = fm_raw.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^(\S[^:]*):\s*(.*)$", line)
        if not m:
            i += 1
            continue
        key = m.group(1).strip()
        rest = m.group(2).strip()
        if rest == "":
            # collect subsequent `- item` lines
            i += 1
            items = []
            while i < len(lines):
                ln = lines[i]
                m2 = re.match(r"^\s*-\s+(.*)$", ln)
                if m2:
                    items.append(parse_scalar(m2.group(1).strip()))
                    i += 1
                else:
                    break
            data[key] = items
            continue
        else:
            data[key] = parse_scalar(rest)
            i += 1

    return data, body


def dump_frontmatter(data: Dict[str, Any]) -> str:
    if yaml:
        fm = yaml.safe_dump(data, sort_keys=False).strip()
    else:
        parts = []
        for k, v in data.items():
            if isinstance(v, list):
                parts.append(f"{k}:")
                for item in v:
                    # represent booleans and other scalars sensibly
                    if isinstance(item, bool):
                        parts.append(f"  - {str(item).lower()}")
                    else:
                        parts.append(f"  - {item}")
            else:
                if isinstance(v, bool):
                    parts.append(f"{k}: {str(v).lower()}")
                else:
                    parts.append(f"{k}: {v}")
        fm = "\n".join(parts)
    return f"---\n{fm}\n---\n"


def normalize_bool(val: Any) -> Any:
    if isinstance(val, bool):
        return val
    if isinstance(val, str):
        s = val.strip().lower()
        if s in ("yes", "y", "true", "t", "1"):
            return True
        if s in ("no", "n", "false", "f", "0"):
            return False
    return val


def normalize_date(val: Any) -> Any:
    if isinstance(val, (datetime, date)):
        return val.isoformat()
    if isinstance(val, str):
        s = val.strip()
        # try ISO first
        try:
            dt = datetime.fromisoformat(s)
            return dt.isoformat()
        except Exception:
            pass
        # common formats
        for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%m/%d/%Y", "%d/%m/%Y"):
            try:
                dt = datetime.strptime(s, fmt)
                return dt.date().isoformat()
            except Exception:
                continue
    return val


def ensure_list(val: Any) -> list:
    if isinstance(val, list):
        return val
    if isinstance(val, str):
        items = [i.strip() for i in re.split(r",\s*", val) if i.strip()]
        return items
    if val is None:
        return []
    return [val]


def migrate_dict(data: Dict[str, Any]) -> Tuple[Dict[str, Any], bool]:
    data = dict(data)  # copy
    changed = False
    alias_map = {
        "author": "authors",
        "created": "date",
        "created_at": "date",
        "updated": "last_modified",
        "modified": "last_modified",
    }

    for alias, canon in alias_map.items():
        if alias in data and canon not in data:
            data[canon] = data[alias]
            del data[alias]
            changed = True

    if "authors" in data:
        new = ensure_list(data["authors"])
        if new != data["authors"]:
            data["authors"] = new
            changed = True

    if "tags" in data:
        new = ensure_list(data["tags"])
        if new != data["tags"]:
            data["tags"] = new
            changed = True

    # normalize booleans
    for k in list(data.keys()):
        v = data[k]
        nv = normalize_bool(v)
        if nv is not v:
            data[k] = nv
            changed = True

    # normalize dates
    for k in ("date", "last_modified"):
        if k in data:
            nv = normalize_date(data[k])
            if nv != data[k]:
                data[k] = nv
                changed = True

    return data, changed


def migrate_text(text: str) -> Tuple[str, bool]:
    data, body = parse_frontmatter(text)
    if not data:
        return text, False
    new_data, _ = migrate_dict(data)
    new_text = dump_frontmatter(new_data) + body
    changed = new_text != text
    return new_text, changed


def process_file(path: str, apply: bool = False, backup_ext: str = ".bak") -> bool:
    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()
    new_text, changed = migrate_text(text)
    if not changed:
        return False
    if apply:
        with open(path + backup_ext, "w", encoding="utf-8") as fh:
            fh.write(text)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(new_text)
    return True


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Migrate wiki frontmatter")
    p.add_argument("--path", "-p", default=".", help="root path to search")
    mode = p.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="dry-run, report changes")
    mode.add_argument("--apply", action="store_true", help="apply changes and create backups")
    p.add_argument("--backup-ext", default=".bak", help="extension for backup files")
    args = p.parse_args(argv)

    if yaml is None:
        # still functional; keep informative message but do not abort
        print("Note: PyYAML not installed; using lightweight fallback parser.", file=sys.stderr)

    changed_files = []
    for dirpath, _, files in os.walk(args.path):
        for fname in files:
            if not fname.endswith(".md"):
                continue
            full = os.path.join(dirpath, fname)
            with open(full, "r", encoding="utf-8") as fh:
                text = fh.read()
            new_text, changed = migrate_text(text)
            if changed:
                changed_files.append(full)
                if args.apply:
                    with open(full + args.backup_ext, "w", encoding="utf-8") as fh:
                        fh.write(text)
                    with open(full, "w", encoding="utf-8") as fh:
                        fh.write(new_text)

    if args.check:
        if changed_files:
            for f in changed_files:
                print(f)
            return 1
        print("No changes detected")
        return 0

    if args.apply:
        print(f"Applied changes to {len(changed_files)} files")
    else:
        print(f"{len(changed_files)} files would change")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
#!/usr/bin/env python3
"""Generate candidate YAML frontmatter for wiki pages (dry-run by default).

Writes `scripts/migration_candidates.json` with suggested frontmatter for
each page under `docs/wiki/tools/`.
"""

import argparse
import json
import os
import sys


def extract_title_and_summary(path):
    try:
        s = open(path, encoding="utf-8").read()
    except Exception:
        return None, None
    lines = s.splitlines()
    title = None
    summary_lines = []
    in_summary = False
    for i, line in enumerate(lines[:50]):
        if line.startswith("#") and not title:
            title = line.lstrip("#").strip()
            in_summary = True
            continue
        if in_summary:
            if line.strip() == "":
                break
            summary_lines.append(line.strip())
    summary = " ".join(summary_lines).strip() if summary_lines else ""
    return title, summary


def extract_live_mapping(path):
    try:
        s = open(path, encoding="utf-8").read()
    except Exception:
        return None
    lines = s.splitlines()
    for i, line in enumerate(lines):
        stripped = line.strip()
        # bolded inline section like "**Live mapping:** ..."
        if stripped.lower().startswith("**live mapping:**"):
            rest = stripped[len("**live mapping:**") :].strip()
            if rest:
                return rest
            # collect following paragraph lines
            mapping_lines = []
            for j in range(i + 1, len(lines)):
                lj = lines[j].strip()
                if not lj or lj.startswith("#") or lj.startswith("**") or lj.startswith("##"):
                    break
                mapping_lines.append(lj)
            return " ".join(mapping_lines).strip() or None
        # heading-style: "Live mapping:" or "## Live mapping:"
        if "live mapping:" in stripped.lower():
            pos = stripped.lower().find("live mapping:")
            rest = stripped[pos + len("live mapping:") :].strip()
            if rest:
                return rest
            mapping_lines = []
            for j in range(i + 1, len(lines)):
                lj = lines[j].strip()
                if not lj or lj.startswith("#") or lj.startswith("**") or lj.startswith("##"):
                    break
                mapping_lines.append(lj)
            return " ".join(mapping_lines).strip() or None
    return None


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args(argv)

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    wiki_root = os.path.join(repo_root, "docs", "wiki", "tools")
    out_path = os.path.join(os.path.dirname(__file__), "migration_candidates.json")

    candidates = []
    if not os.path.isdir(wiki_root):
        print("No wiki tools folder found at", wiki_root)
        return 1
    for root, _, files in os.walk(wiki_root):
        for fn in files:
            if not fn.endswith(".md"):
                continue
            path = os.path.join(root, fn)
            rel = os.path.relpath(path, repo_root)
            title, summary = extract_title_and_summary(path)
            live_map = extract_live_mapping(path)
            candidates.append(
                {
                    "path": rel,
                    "title": title or os.path.splitext(fn)[0],
                    "summary": summary,
                    "live_mapping": live_map,
                }
            )
            if args.apply:
                # insert a minimal frontmatter if missing
                s = open(path, encoding="utf-8").read()
                if not s.lstrip().startswith("---"):
                    # build frontmatter lines, include Live mapping when present
                    fm_lines = ["---"]
                    fm_lines.append('name: "{}"'.format((title or fn).replace('"', '\\"')))
                    fm_lines.append('summary: "{}"'.format(summary.replace('"', '\\"')))
                    if live_map:
                        fm_lines.append('Live mapping: "{}"'.format(live_map.replace('"', '\\"')))
                    fm_lines.append("---")
                    fm = "\n".join(fm_lines) + "\n\n"
                    open(path, "w", encoding="utf-8").write(fm + s)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"candidates": candidates}, f, indent=2)
    print("Wrote", out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
