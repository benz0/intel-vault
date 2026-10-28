---
# Vault configuration. Every AI reads this at the start of a session.
# Keep values flat (key: value, or key: [a, b]) so the scripts can read it.
# Every setting goes inside this block, between the two --- lines. Lines below the
# closing --- are notes for humans; scripts never read them.

owner_name:            # e.g. Jordan Lee
owner_initials:        # e.g. JL (used to sign CRM and timeline entries)
owner_role:            # e.g. Customer Success Engineer
organization:          # employer or team
manager:               # who the owner reports to
priority_senders: []   # people whose email always counts as an ask, besides the manager (used by the inbox workflow), e.g. [Pat Smith, pat@example.com]
timezone:              # IANA name, e.g. America/New_York. All times are stated in this zone first.

forbidden_chars: []    # characters that must never appear in vault files, e.g. [U+2014] for em dashes
forbidden_chars_allow: []  # exact strings exempt from that check, e.g. a signature line
check_exclude: []      # folders check-vault.py skips: a name matches anywhere (e.g. _Backups), a path with / matches from the root
check_raw_dirs: [Sources]  # raw source folders: links checked, forbidden characters not (sources are saved unedited)

packs: []              # installed packs, e.g. [cse]
agents: []             # AI tools that work in this vault, e.g. [claude, copilot]

# Where things live, relative to the vault root
task_list: Open Actions.md
sessions_dir: _Sessions
internal_dir: _Internal
accomplishments: _Internal/Accomplishments.md
feedback_log: _Internal/Feedback Received.md
inbox_dir: _Inbox
drafts_dir: Drafts

# Data policy: the short version of what your employer allows in AI tools.
# Rules in _system/rules/20-data-handling.md apply on top of this.
data_policy:           # e.g. "No customer account numbers. No employee performance details."

# Optional: for an AI tool that only reads rules, skills, or commands from its own folder.
# _system/scripts/export-agent-files.py writes copies there. Leave blank if unused.
export_rules_dir:
export_skills_dir:
export_commands_dir:
export_alias_skills:          # true: also write a small skill per alias (for tools whose slash commands come from skills)
export_user_only: []          # workflows the tool should only run when asked
export_user_only_frontmatter: # file with the tool-specific frontmatter lines for those skills

# Optional: publish a read-only copy for AI tools that only read cloud storage
# (for example Microsoft 365 Copilot). Point publish_dir at an EMPTY folder that
# OneDrive or SharePoint syncs, outside this vault. Runs after wrap and intake.
publish_dir:
publish_exclude: [_system/local, _Internal]
publish_layout: mirror     # mirror (keep folders) or flat (experimental: one folder, names joined with " - ")
---

# Vault configuration

The values above are the source of truth. This section is notes for humans.

- **Settings go above, inside the `---` block.** A setting typed down here is ignored.
- **Change a path here, not in the rules.** Rules refer to files by their config name.
- **`packs`** is maintained by `scripts/update-vault.py`. Edit it only to remove a pack.
- **Owner preferences** (writing style, signature, formatting needs) go in `_system/local/rules/10-owner.md`, not here.
