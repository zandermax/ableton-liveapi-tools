# 02 — Migrate wiki frontmatter

Status
- Completed (2026-05-18): `scripts/migrate_wiki_frontmatter.py` implemented, unit tests added, CLI supports `--check`/`--apply`, changes committed.

Overview
- Normalize YAML frontmatter across wiki pages. Idempotent, reversible, safe.

Scope
- Target markdown files exported from wiki (`*.md`) used as source-of-truth.
- Focus on docs, planning, and wiki folders (scoped via CLI `--path`).

Implementation summary
- `scripts/migrate_wiki_frontmatter.py` (Python):
	- Parses frontmatter using PyYAML when available, falls back to lightweight parser.
	- Normalizes aliases (`author` → `authors`, `created`/`created_at` → `date`, `updated`/`modified` → `last_modified`).
	- Normalizes dates to ISO-8601, booleans to true/false, and ensures list fields (`tags`, `authors`) are arrays.
	- Provides `--check` (dry-run) and `--apply` (write changes, create `.bak` backups) modes.

Tests
- Unit tests: `tests/test_migrate_frontmatter.py` covering alias mapping, date/boolean/list normalization, idempotence, and CLI behavior.
- Run: `pytest tests/test_migrate_frontmatter.py -q` (or full `pytest`).

Usage
```bash
# dry-run: list files that would change
python3 scripts/migrate_wiki_frontmatter.py --check --path planning/wiki-as-source-of-truth

# apply changes (creates .bak backup next to each file)
python3 scripts/migrate_wiki_frontmatter.py --apply --path planning/wiki-as-source-of-truth
```

Deliverables
- `scripts/migrate_wiki_frontmatter.py` (CLI)
- `tests/test_migrate_frontmatter.py`

Changelog
- 2026-05-18: Implemented script + tests + CLI; tests pass and changes committed.

