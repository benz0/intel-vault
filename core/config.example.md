---
# Vault configuration. Every AI reads this at the start of a session.
# Keep values flat (key: value, or key: [a, b]) so the scripts can read it.

owner_name:            # e.g. Jordan Lee
owner_initials:        # e.g. JL (used to sign CRM and timeline entries)
owner_role:            # e.g. Customer Success Engineer
organization:          # employer or team
manager:               # who the owner reports to
timezone:              # IANA name, e.g. America/New_York. All times are stated in this zone first.

forbidden_chars: []    # characters that must never appear in vault files, e.g. [U+2014] for em dashes

packs: []              # installed packs, e.g. [cse]
agents: []             # AI tools that work in this vault, e.g. [claude, bob]

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
---

# Vault configuration

The values above are the source of truth. This section is notes for humans.

- **Change a path here, not in the rules.** Rules refer to files by their config name.
- **`packs`** is maintained by `scripts/update-vault.py`. Edit it only to remove a pack.
- **Owner preferences** (writing style, signature, formatting needs) go in `_system/local/rules/10-owner.md`, not here.
