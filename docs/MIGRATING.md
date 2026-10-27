# Adopting an existing vault

For anyone who already keeps AI-maintained notes (an Obsidian vault, a folder of markdown, a tool-specific rules folder) and wants to move them onto intel-vault **without moving or rewriting the notes themselves.**

The rule for the whole process: **your notes are never touched.** Only the instruction layer changes: a new `_system/` folder, plus whatever folder your AI tool reads its rules from.

Keep a `MIGRATION-LOG.md` in your backup folder as you go: each step, what worked, what did not, and anything these docs got wrong. Send the "got wrong" items back as issues.

---

## 0. Before you start

- **Close every AI tool that writes to the vault.** Nothing else should change files while you migrate.
- **Inventory what you have today:** every rule file, skill, command, script, and any tool-specific folder (for example a hidden folder your assistant loads rules from). List each one; you will map every item to its new home in step 4.
- **List every command you use day to day.** After the migration, every one of them must still work. This is your acceptance test.

## 1. Back up, and write the rollback note first

1. Make a backup folder inside the vault, for example `_Backups/YYYY-MM-DD-intel-vault-migration/`.
2. Copy into it, unchanged: your tool's rules/skills/commands folder, `AGENTS.md` (or your equivalent entry file), and any root docs that describe the old setup.
3. **Verify the copy with a file count and `diff -rq`, never by eye.** On network shares (a NAS, SMB, some cloud-synced folders) `cp -p` can fail on a single file without stopping the copy, because the share refuses the permission change. A plain `cp` (or `cp -R`) is safer there.
4. **Write `ROLLBACK.md` in that folder before changing anything.** Use the template below, filled in with your real paths.

### ROLLBACK.md template

```markdown
# Rollback: intel-vault migration, YYYY-MM-DD

Backed up here, unchanged: {list every file and folder copied}

## Roll back if
- Your assistant cannot state your formatting rules, your manager, and your commands
- A command you use daily is missing or behaves differently
- Any acceptance check in MIGRATION-LOG.md fails and cannot be fixed in place

## Steps
1. Close every AI tool that writes to the vault.
2. Restore the tool folder: replace {tool folder} with the copy in this backup.
3. Restore {AGENTS.md and root docs} from this backup.
4. Move `_system/` into this backup folder as `_system-rolledback/` (do not delete it; it holds what was learned).
5. Restore any assistant skill or custom instructions you changed (copies saved here).
6. Open your assistant and ask: "What are my formatting rules, who is my manager, and which commands do you have?" The old answers mean the rollback worked.

Your notes were never modified, so no note needs restoring.
```

## 2. Get the repo

```bash
git clone https://github.com/benz0/intel-vault.git
```

## 3. Adopt

Point the config at the files you already have:

```bash
python3 intel-vault/scripts/new-vault.py /path/to/your/vault --adopt --packs cse \
  --owner "Your Name" --initials YN --role "Your Role" --org "Your Org" \
  --manager "Manager Name" --tz America/New_York --agents claude \
  --task-list "path/to/your task list.md" --sessions-dir "your sessions folder" \
  --internal-dir "your internal folder"
```

`--adopt` writes only `_system/`. It warns if a path in config does not exist yet. Then open `_system/config.md` and finish it (data policy, optional files, export folders). **Every setting goes inside the block between the two `---` lines at the top;** anything typed below it is ignored by the scripts.

## 4. Move your own rules into `_system/local/`

Map every item from your step 0 inventory:

| Kind of item | Goes to |
|---|---|
| Who you are, your style, signature, vocabulary | `_system/local/rules/` |
| Your employer's process (risk model, field values, approvals) | `_system/local/rules/30-{employer}-process.md` |
| Conventions the core already covers | Drop them, **but keep anything specific to you** (your field names, your real-case examples) in a trimmed local rule |
| A workflow the core or a pack already has | Use the shared one. If yours does something the shared one does not, put the difference in a local rule or a local workflow of the same name |
| A workflow that is only yours | `_system/local/workflows/` (scripts it needs: `_system/local/scripts/`) |
| Templates whose field names your old notes rely on | `_system/local/templates/` with the same file name as the core template |

**Nothing from the inventory may be left unmapped.** Mark each line in the log with where it went.

## 5. Connect your assistants

- **Assistants that read the folder:** point them at `_system/README-for-AI.md` (see `adapters/`).
- **Assistants that only load their own rules folder:** set `export_rules_dir`, `export_skills_dir`, `export_commands_dir` in config, move the old contents of those folders into the backup, then run `python3 _system/scripts/export-agent-files.py`. It reports any hand-written file it finds instead of overwriting it.
- **Check that every old command name still appears in the tool's command list,** not only the new names. Some tools build their slash-command list from the skills folder and ignore a commands folder. If old names are missing, set `export_alias_skills: true` (plus `export_user_only_frontmatter` with your tool's "do not auto-run" lines) and export again.

## 6. Check

1. `python3 _system/scripts/check-vault.py` and record the counts. Older notes often have issues; record them, do not mass-fix them during the migration. Put legacy folders you do not want checked (old exports, `_Backups`) in `check_exclude` in config. Raw `Sources/` are checked for links only.
2. Ask each assistant: "What are my formatting rules, who is my manager, and which commands do you have?"
3. Run your daily commands from step 0 on a real subject (`resume`, `prep`, and one `intake` at minimum).
4. Record every result in the log. Any failure is either fixed in place or a rollback trigger.

## 7. Afterward

- Keep the backup until you have worked a full week on the new setup.
- Update to new repo versions with `scripts/update-vault.py`; it never touches `_system/local/` or `config.md`.
