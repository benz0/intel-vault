# IBM Bob adapter

Bob loads `.bob/rules/` automatically on every message and offers `.bob/skills/` and `.bob/commands/` as slash commands. In an intel vault those are **generated** from `_system/`, which stays the single source of truth for every agent.

## Setup

1. Open the vault folder itself in Bob (File > Open Folder). Not a parent folder: Bob only loads `.bob/` from the workspace root.
2. Generate Bob's files:

   ```
   python3 _system/scripts/sync-bob.py
   ```

3. Optional: copy `custom_modes.example.yaml` from this folder to `.bob/custom_modes.yaml` and edit the role text. It gives Bob three modes: a working mode that can only edit markdown, a read-only analyst mode for anything that reaches a customer or leadership, and a drafting mode.
4. Verify it loaded. Ask Bob: *"What are my formatting rules, who is my manager, and which commands do you have?"* If it cannot answer from your config and local rules, the rules did not load.

## After any change to `_system/`

Re-run `sync-bob.py`. It overwrites only files carrying its GENERATED banner, removes generated files whose source is gone, and reports anything else as a conflict instead of touching it.

**Do not edit `.bob/rules/` by hand.** The next sync overwrites it. Put your own rules in `_system/local/rules/` and your own workflows in `_system/local/workflows/`, then sync.

## Lessons from running Bob on a vault

- **Never move rule files with a delete behind an unverified copy.** One vault lost its formatting rule that way and the next build produced hundreds of violations. Copy, verify, then delete.
- **Bob's file edits are reliable; its counts and citations are not.** It has reported zero broken links and zero forbidden characters when neither was true, usually by leaving its own output out of its own check. Run `_system/scripts/check-vault.py` yourself.
- **Start a new Bob task per subject.** One context across many accounts invites bleed between them.
- **Data rules:** Bob's usage guidelines prohibit sensitive personal information, health information, regulated financial data, and secrets. Keep any personal vault out of Bob's workspace entirely.
