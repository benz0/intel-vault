# Changelog

## 0.3.3 (2026-10-27)

From the first update of a migrated vault.

- **Exporter:** `export_alias_skills: true` writes a small wrapper skill for each alias, for tools whose slash commands come only from the skills folder (old command names stopped appearing otherwise). Generated files whose source still exists are left in place and reported, so the exporter never fights a tool that derives files from ours.
- `check-vault.py`: relative links (`[[../Stakeholders/Jane Doe]]`) resolve as in Obsidian.
- `update-vault.py`: ignores Python cache files.
- `intake`: move both the email's markdown copy and the original file into `Sources/`.
- `email-to-md.py`: file names drop leading tags such as `[EXTERNAL]` as well as RE/FW.
- `prep`: state the meeting date relative to today; never "today's call" unless it is.
- Config and MIGRATING: settings go inside the `---` block; check every old command name after export.

## 0.3.2 (2026-10-27)

From the first migration of a real vault (about 1,800 files).

- `check-vault.py`: links written with the extension (`[[Account Overview.md]]`) now resolve, as they do in Obsidian. Raw source folders (`check_raw_dirs`, default `Sources`) are checked for links but not forbidden characters. New `check_exclude` config key and `--exclude` flag to skip legacy folders.
- `resume`: reconciles the task list against newer session logs and lists tasks that look done instead of reporting them overdue.
- `docs/MIGRATING.md`: verify backups with `diff -rq`; `cp -p` can fail silently on network shares.

## 0.3.1 (2026-10-27)

- `new-vault.py --adopt` for existing vaults: writes only `_system/`, with path options so config points at files you already have.
- `docs/MIGRATING.md`: adoption steps with a backup, a written rollback plan, and acceptance checks.
- Templates layer like rules: `_system/local/templates/` overrides pack and core templates.
- Exporter: `export_user_only` and `export_user_only_frontmatter` mark skills a tool should run only when asked.

## 0.3.0 (2026-10-27)

From a working session with two CSEs who run their own versions of this workflow.

- **Email as a source:** `email-to-md.py` converts saved `.eml` and Outlook `.msg` files into markdown sources (attachments listed, not read). `.msg` needs `extract-msg`.
- **`intake-batch`:** process a backlog in planned, resumable batches with a spot-check of each batch against its sources.
- **CSE pack:** `MEDDPICC.md` and `Account Plan.md` are now opt-in (`cse_optional_files`). New `CSE Dashboard.md` template.
- **`cs-update`:** activity fields up front (title, date, time, duration, internal and external attendees); never cite the source file or link contacts in the entry.
- **`build-vault`:** seed history from a CRM or customer-success platform export.
- **Publishing:** experimental `publish_layout: flat` for assistants that struggle with deep folders.
- **README:** a no-cost setup, and credits.

## 0.2.0 (2026-10-27)

- **Readers and writers.** `publish-vault.py` mirrors the vault one way into a cloud-synced folder (`publish_dir`) for assistants that cannot reach it, such as Microsoft 365 Copilot. `intake` and `wrap` publish automatically. `_system/local` and `_Internal` are excluded by default.
- **Capture notes** (`_system/templates/capture.md`): the fixed format a read-only assistant uses to hand back new information. `intake` treats them as proposals.
- `adapters/m365-copilot.md`: setup, reader instructions, the M365 "what's new" sweep, and what was tested.

## 0.1.2 (2026-10-27)

- README rewritten for a first-time reader: the problem, what it does for a CSE, guardrails.
- `examples/demo-vault/`: a small fictional vault showing intake, prep, a session log, and the task list.

## 0.1.1 (2026-10-26)

- Removed all tool-specific adapters except the Claude skill. Tools that only read their own rules folder use the new generic `export-agent-files.py` (configured with `export_rules_dir`, `export_skills_dir`, `export_commands_dir`).
- `forbidden_chars_allow` exempts exact strings (for example a signature) from the forbidden-character check.

## 0.1.0 (2026-10-26)

First release: core spec, CSE pack, Claude adapter, any-LLM prompt, and the new-vault, update-vault, check-vault, and sheet-to-md scripts.
