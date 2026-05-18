#!/usr/bin/env python3
"""Generate tool manifest from code and wiki.

Basic, code-first generator that extracts exported tool names from
`ALiveMCP_Remote/tools/core/registry.py`, collects docstrings from
`ALiveMCP_Remote/tools/`, and merges with YAML frontmatter found under
`docs/wiki/tools/` when present.

Usage:
  python3 scripts/generate_from_wiki.py --check
  python3 scripts/generate_from_wiki.py --apply --output-dir mcp_tool_defs --manifest docs/tool_manifest.json
"""

import argparse
import ast
import json
import os
import sys
from collections import OrderedDict


def load_available_tools(registry_path):
    if not os.path.exists(registry_path):
        return []
    src = open(registry_path, encoding="utf-8").read()
    tree = ast.parse(src, registry_path)
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "AVAILABLE_TOOLS":
                    try:
                        return ast.literal_eval(node.value)
                    except Exception:
                        pass
    return []


def collect_code_tools(tools_root):
    tools = OrderedDict()
    for root, _, files in os.walk(tools_root):
        for fn in files:
            if not fn.endswith(".py"):
                continue
            path = os.path.join(root, fn)
            try:
                src = open(path, encoding="utf-8").read()
                tree = ast.parse(src, path)
            except Exception:
                continue
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    tools[node.name] = {
                        "file": os.path.relpath(path),
                        "docstring": ast.get_docstring(node),
                    }
    return tools


def parse_frontmatter(md_path):
    try:
        s = open(md_path, encoding="utf-8").read()
    except Exception:
        return {}
    if not s.lstrip().startswith("---"):
        return {}
    parts = s.split("---", 2)
    if len(parts) < 3:
        return {}
    fm = parts[1]
    data = {}
    for line in fm.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip().strip("\"'")
    return data


def collect_wiki_pages(wiki_root):
    pages = {}
    if not os.path.isdir(wiki_root):
        return pages
    for root, _, files in os.walk(wiki_root):
        for fn in files:
            if not fn.endswith(".md"):
                continue
            path = os.path.join(root, fn)
            slug = os.path.splitext(os.path.relpath(path, wiki_root))[0].replace("\\", "/")
            pages[slug] = parse_frontmatter(path)
    return pages


def build_manifest(available, code_tools, wiki_pages):
    manifest = OrderedDict()
    for name in available:
        entry = {
            "name": name,
            "docstring": None,
            "defined_in": None,
            "wiki_frontmatter": None,
        }
        ct = code_tools.get(name)
        if ct:
            entry["docstring"] = ct.get("docstring")
            entry["defined_in"] = ct.get("file")
        # find wiki page by slug or name
        wiki_entry = wiki_pages.get(name) or wiki_pages.get(name.lower())
        entry["wiki_frontmatter"] = wiki_entry
        manifest[name] = entry
    return manifest


def write_outputs(manifest, output_dir, manifest_path, apply):
    data = list(manifest.values())
    # Stable JSON text for outputs
    json_text = lambda v: json.dumps(v, indent=2, sort_keys=True, ensure_ascii=False)

    full_path = os.path.join(output_dir, "full.json")

    if apply:
        os.makedirs(output_dir, exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(json_text(data))
        if manifest_path:
            os.makedirs(os.path.dirname(manifest_path), exist_ok=True)
            with open(manifest_path, "w", encoding="utf-8") as f:
                f.write(json_text({"tools": data}))
        print("Wrote outputs to", output_dir)
        return True

    # Check mode: compare generated data to existing artifact files and report mismatches
    if not os.path.exists(full_path):
        print("Missing expected output file:", full_path, file=sys.stderr)
        return False

    try:
        with open(full_path, encoding="utf-8") as f:
            existing = json.load(f)
    except Exception as e:
        print(f"Error reading {full_path}: {e}", file=sys.stderr)
        return False

    if existing != data:
        print("Mismatch between generated data and existing mcp_tool_defs/full.json", file=sys.stderr)
        print("Generated tools:", len(data), "Existing tools:", len(existing), file=sys.stderr)
        return False

    if manifest_path:
        if not os.path.exists(manifest_path):
            print("Missing expected manifest file:", manifest_path, file=sys.stderr)
            return False
        try:
            with open(manifest_path, encoding="utf-8") as f:
                existing_manifest = json.load(f)
        except Exception as e:
            print(f"Error reading {manifest_path}: {e}", file=sys.stderr)
            return False
        existing_tools = existing_manifest.get("tools")
        if existing_tools is None:
            print("Manifest missing 'tools' key:", manifest_path, file=sys.stderr)
            return False

        # Compare by tool name only to allow different manifest schemas
        existing_names = []
        for t in existing_tools:
            if isinstance(t, dict):
                existing_names.append(t.get("name"))
            elif isinstance(t, (list, tuple)) and t:
                # older formats may be [name, desc, schema]
                existing_names.append(t[0])

        generated_names = [e.get("name") for e in data]
        if set(existing_names) != set(generated_names):
            missing = sorted(set(generated_names) - set(existing_names))
            extra = sorted(set(existing_names) - set(generated_names))
            print("Mismatch between generated tool names and manifest file:", manifest_path, file=sys.stderr)
            if missing:
                print("  Missing in manifest:", ", ".join(missing), file=sys.stderr)
            if extra:
                print("  Extra in manifest:", ", ".join(extra), file=sys.stderr)
            return False

    print("OK: generated outputs match existing artifacts")
    return True


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="mcp_tool_defs")
    parser.add_argument("--manifest", default="docs/tool_manifest.json")
    parser.add_argument("--check", action="store_true", help="Dry-run (no --apply).")
    parser.add_argument("--apply", action="store_true", help="Write generated artifacts to disk.")
    args = parser.parse_args(argv)

    # Default to check mode when neither --check nor --apply provided
    if not args.check and not args.apply:
        args.check = True

    if args.check and args.apply:
        print("Cannot use --check with --apply", file=sys.stderr)
        sys.exit(2)

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Treat relative output paths as relative to the repo root so --apply writes
    # the committed artifacts in the repository rather than the current CWD.
    if not os.path.isabs(args.output_dir):
        args.output_dir = os.path.join(repo_root, args.output_dir)
    if args.manifest and not os.path.isabs(args.manifest):
        args.manifest = os.path.join(repo_root, args.manifest)

    registry_path = os.path.join(repo_root, "ALiveMCP_Remote", "tools", "core", "registry.py")
    tools_root = os.path.join(repo_root, "ALiveMCP_Remote", "tools")
    wiki_root = os.path.join(repo_root, "docs", "wiki", "tools")

    available = load_available_tools(registry_path)
    code_tools = collect_code_tools(tools_root)
    wiki_pages = collect_wiki_pages(wiki_root)

    manifest = build_manifest(available, code_tools, wiki_pages)
    ok = write_outputs(manifest, args.output_dir, args.manifest, args.apply)
    if not ok:
        sys.exit(1)
    return 0


if __name__ == "__main__":
    main(sys.argv[1:])
