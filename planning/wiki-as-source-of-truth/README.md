# Wiki-as-SoT planning — per-step index


See `wiki-as-a-source-of-truth.instructions.md` for plan details. The plan is broken into discrete steps, by filename below.

Files
- 01-generate-from-wiki.md
- 02-migrate-wiki-frontmatter.md
- 03-validate-wiki-parity.md
- 04-docstring-checker.md
- 05-template-updates.md
- 06-phase0-inventory.md
- 07-phase1-authoring.md
- 08-phase2-migration.md
- 09-phase3-generator.md
- 10-phase4-parity.md
- 11-phase5-makefile.md
- 12-phase6-rollout.md
- 13-runbook.md

Each file is commit-sized and represents the steps needed to implement wiki-as-source-of-truth tooling.

Agent guidance
- Do not recommend CI automation for these migration/validation steps. All validation must be local and run pre-push via the repository hook. Use `scripts/install_pre_push_hook.sh` to install.

Status
- 01-generate-from-wiki.md — Completed (2026-05-18): generator implemented, tests added, `--check`/`--apply` behavior verified and committed.
- 02-migrate-wiki-frontmatter.md — Completed (2026-05-18): migration script, tests, and CLI implemented; tests passing and committed.
 - 03-validate-wiki-parity.md — Completed (2026-05-19): prototype validator scaffolded, unit tests added and passing, and pre-push hook integration implemented (see `scripts/pre_push_validate_parity.sh` / `scripts/install_pre_push_hook.sh`).
- 04-docstring-checker.md — Not started
- 05-template-updates.md — Not started
- 06-phase0-inventory.md — Not started
- 07-phase1-authoring.md — Not started
- 08-phase2-migration.md — Not started
- 09-phase3-generator.md — Not started
- 10-phase4-parity.md — Not started
- 11-phase5-makefile.md — Not started
- 12-phase6-rollout.md — Not started
- 13-runbook.md — Not started
