# Changelog

## 0.1.1 (2026-10-26)

- Removed all tool-specific adapters except the Claude skill. Tools that only read their own rules folder use the new generic `export-agent-files.py` (configured with `export_rules_dir`, `export_skills_dir`, `export_commands_dir`).
- `forbidden_chars_allow` exempts exact strings (for example a signature) from the forbidden-character check.

## 0.1.0 (2026-10-26)

First release: core spec, CSE pack, Claude adapter, any-LLM prompt, and the new-vault, update-vault, check-vault, and sheet-to-md scripts.
