---
# Vault configuration. Every AI reads this at the start of a session.
# Keep values flat (key: value, or key: [a, b]) so the scripts can read it.

owner_name: Jordan Lee  # e.g. Jordan Lee
owner_initials: JL      # e.g. JL (used to sign CRM and timeline entries)
owner_role: Customer Success Engineer  # e.g. Customer Success Engineer
organization: Example Software Co  # employer or team
manager: Pat Morgan     # who the owner reports to
timezone: America/New_York  # IANA name, e.g. America/New_York. All times are stated in this zone first.

forbidden_chars: [U+2014]  # characters that must never appear in vault files, e.g. [U+2014] for em dashes
forbidden_chars_allow: []  # exact strings exempt from that check, e.g. a signature line

packs: [cse]            # installed packs, e.g. [cse]
agents: [claude]        # AI tools that work in this vault, e.g. [claude, copilot]

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
data_policy: "Customer names, architecture, and contract values OK. No credentials, no personal data."

# Optional: for an AI tool that only reads rules, skills, or commands from its own folder.
# _system/scripts/export-agent-files.py writes copies there. Leave blank if unused.
export_rules_dir:
export_skills_dir:
export_commands_dir:

# cse pack
cs_platform: Gainsight
crm: Salesforce
products: [Vault Enterprise, Terraform Enterprise]
competitors: []

---

# Vault configuration

The values above are the source of truth. This section is notes for humans.

- **Change a path here, not in the rules.** Rules refer to files by their config name.
- **`packs`** is maintained by `scripts/update-vault.py`. Edit it only to remove a pack.
- **Owner preferences** (writing style, signature, formatting needs) go in `_system/local/rules/10-owner.md`, not here.
