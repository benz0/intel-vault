# Roadmap

## v0.1 (this release)

- Core: rules, workflows (resume, wrap, intake, prep, brief, internal, review-prep), templates
- CSE pack: account structure, customer-success platform rules, risk, cs-update, build-vault
- Adapters: Claude skill, IBM Bob (generated `.bob/`), any-LLM starter prompt
- Scripts: new-vault, update-vault, sync-bob, check-vault, sheet-to-md

## Next

1. **Migrate the original CSE vault onto v0.1** (the dogfood test). Anything that breaks becomes a fix here.
2. **`se` pack:** opportunity folders, MEDDPICC as the spine, deal reviews, CRM updates drafted for the owner to paste (no CRM connector assumed).
3. **`people-manager` pack:** shaped by an interview with the first user. Expected pieces:
   - `Team/{Name}/` per direct report: 1:1 notes, goals, coaching, wins, follow-ups owed
   - `Accounts/` for accounts the manager assists on
   - Teams transcripts brought in by paste or via `_Inbox/`
   - strict defaults for HR-sensitive content
4. **`personal-life` pack:** areas, one personal task list, sessions. No content shipped.
5. **Copilot adapter,** once tested against a real Microsoft 365 setup.

## Open design questions

- Should `AGENTS.md` be renamed for tools that look for other entry files (for example `CLAUDE.md`, `.github/copilot-instructions.md`)? Today each adapter points its tool at `AGENTS.md`.
- Bob generates wrapper skills for commands. Confirm the generated command and skill sharing a name behaves the same as the hand-built setup did.
