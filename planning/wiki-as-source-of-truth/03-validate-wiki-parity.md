# 03 — Validate Wiki Parity

## Purpose

Ensure generated repository docs (from the wiki generator) remain in parity with the source wiki. This step implements a local validator that detects and optionally repairs drift between canonical generator output and the tracked files.

## Scope

- Files produced by `01-generate-from-wiki.md` (generator output)
- Wiki frontmatter and canonical content used as the source of truth
- Exclude intentionally-volatile fields (configurable), e.g. `last_updated` timestamps

## Requirements

- Local-only validation; do not mandate CI enforcement. All validation runs must be possible locally and via the repository pre-push hook.
- CLI must support `--check` (read-only, exit non-zero on differences) and `--apply` (mutate files to match generator output).
- Produce clear, human-friendly diffs with file paths and small context so authors can review changes before applying.
- Tests (unit + integration) must exist and run locally.

## Acceptance Criteria

- `scripts/validate-wiki-parity.py --check` returns exit code 0 when files match and non-zero when parity violations exist.
- `scripts/validate-wiki-parity.py --apply` updates repository files to match canonical generator output.
- Tests covering parity rules and a small set of fixtures are added under `planning/tests/` and pass locally.
- Pre-push hook (installed via `scripts/install_pre_push_hook.sh`) runs the validator in `--check` mode by default.

## Implementation Plan (next actions)

1. Define parity rules
   - Enumerate which fields must match exactly (title, body, selected frontmatter keys) and which are excluded.
   - Create a small JSON/YAML config for exclusions and special-casing.

2. Build compare engine
   - Reuse the output of the generator (step 01) as the canonical form.
   - Normalize both sides (trim, canonicalize frontmatter order, strip excluded keys) before diffing.
   - Use a text diff for body and structural checks for frontmatter keys.

3. CLI scaffold
   - Add `scripts/validate-wiki-parity.py` implementing `--check`, `--apply`, `--verbose`, and `--files` flags.
   - Ensure the script returns proper exit codes and prints a short summary and per-file diffs.

4. Tests & fixtures
   - Add fixtures in `planning/tests/fixtures/` for matching and mismatched cases.
   - Add unit tests for the normalization and compare functions and an integration test invoking the CLI.

5. Hook integration & docs
   - Update `scripts/install_pre_push_hook.sh` (or document how to call it) to run the validator in `--check` mode.
   - Add short usage docs to `planning/README.md` and this file.

## How to run locally (dev)

Install Python 3.x if needed; then from repository root:

```bash
# Check parity (non-destructive)
python3 scripts/validate-wiki-parity.py --check

# Apply canonical changes (destructive)
python3 scripts/validate-wiki-parity.py --apply

# Install pre-push hook (calls validator in --check)
scripts/install_pre_push_hook.sh
```

## Notes / Pitfalls

- Some frontmatter keys are intentionally divergent between generator output and hand-edited files; keep an allowlist for these.
- Keep the validator fast by comparing only files impacted by the generator or changed in the index; provide a `--files` filter.
- Do not enable automatic hook installation in CI; keep installation a local maintainer action.

## Next proposal

I can scaffold `scripts/validate-wiki-parity.py` (minimal CLI + compare engine) and add a couple of fixtures/tests next — confirm and I'll implement the prototype.
# 03 — Validate wiki parity

Overview
- Ensure generated docs (from wiki) remain in parity with canonical wiki pages. Detect divergences introduced by generator, manual edits, or tooling changes.

Goals
- Compute content-level signature for each source wiki page and corresponding generated artifact.
- Report mismatches with brief diff snippets and metadata (frontmatter differences, missing pages, extra files).
- Provide `--check` mode (CI-friendly, non-mutating), `--json` output for automation, and `--fix` hints (rerun generator or reconcile changes).

Scope
- Default source: `docs/wiki` (wiki export). Default target: `_Node/webui` (generated docs).
- Do not scan `planning/` by default; pass `--allow-planning` to explicitly allow scanning planning paths.

Implementation notes
- Prototype script: `scripts/validate_wiki_parity.py`.
  - Parse frontmatter and body using shared parser utilities.
  - Normalize both sides (canonicalize frontmatter, trim whitespace) before comparison.
  - Matching modes: `--match-by rel|basename`.
  - Explicit mappings: `--map source_rel:target_rel` (repeatable).
  - Output modes: human summary (default) and `--json` for machine-readable reports.

Tests
- Unit tests: `tests/test_validate_wiki_parity.py`.
- Fixtures: `tests/fixtures/validate-parity/` (add as needed).

Commands (dev)
```bash
# run unit tests
pytest tests/test_validate_wiki_parity.py -q

# dry-run: default paths
python3 scripts/validate_wiki_parity.py --check --source docs/wiki --target _Node/webui

# match by basename when generator relocates files
python3 scripts/validate_wiki_parity.py --check --match-by basename --source docs/wiki --target _Node/webui

# explicit mapping for a single file
python3 scripts/validate_wiki_parity.py --check --map "01-generate-from-wiki.md:docs/01-generate-from-wiki.md" --source docs/wiki --target _Node/webui

# allow scanning planning/ only when intentional
python3 scripts/validate_wiki_parity.py --check --source planning/wiki-as-source-of-truth --allow-planning --target _Node/webui

# json output + fail CI on mismatch
python3 scripts/validate_wiki_parity.py --json --fail-on-mismatch --check --source docs/wiki --target _Node/webui
```

Deliverables
- `scripts/validate_wiki_parity.py` prototype
- `tests/test_validate_wiki_parity.py` + fixtures
- Local pre-push hook to run parity validators (see below)

Plan
1. Finalize mapping rules for common generator relocations.
2. Provide local pre-push hook to run validators before pushing.
3. Improve reports: per-file diff snippets, summarized counts, and optional archived artifacts.

Verification
- `--check` lists mismatches and returns non-zero on mismatch.
- `--json` emits structured report for local consumption.

Commit message
- feat(docs): clarify parity validator doc, default paths, examples

Pre-push hook (local)

Purpose
- Run parity validations locally before allowing `git push`. Avoid CI dependencies; keep validation local and fast.

Install (one-time on developer machine)
```bash
cd /path/to/alivemcp
bash scripts/install_pre_push_hook.sh
```

Behavior
- Runs `scripts/validate_registry_parity.py --check` (registry ↔ code ↔ wiki). Fails push on mismatch.
- If generated-site target exists (example `_Node/webui`), runs `scripts/validate_wiki_parity.py --check --source docs/wiki --target _Node/webui` and fails push on mismatch.
- If target missing, the hook prints a warning and allows push (so developers who don't build site locally aren't blocked).

Hook files
- `scripts/pre_push_validate_parity.sh`: entrypoint for hook logic.
- `scripts/install_pre_push_hook.sh`: installs hook into `.git/hooks/pre-push` and makes it executable.

Notes for agents
- Do not propose CI-based automation for parity validation. Suggest local pre-push hook or manual invocation only.
