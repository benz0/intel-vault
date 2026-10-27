# Demo vault

A small, working example of an intel vault for a CSE. **Everything here is fictional:** the company, the people, the figures, and the transcript.

It shows one account, Bluefin Logistics, a few days after a customer call:

| File | Shows |
|---|---|
| `AGENTS.md` | The one-row-per-account view every AI reads first |
| `Open Actions.md` | The single task list, each item with a source and date, other people's commitments under "Waiting on others" |
| `Accounts/Bluefin Logistics/Sources/` | Raw material, saved untouched |
| `Accounts/Bluefin Logistics/Vault Enterprise/Meetings/` | The meeting record written from that transcript |
| `Accounts/Bluefin Logistics/Current State.md` | Dated status blocks, newest first, with confidence tags |
| `Accounts/Bluefin Logistics/_Prep/` | A call prep brief for the next meeting |
| `_Sessions/` | A session log with a drafted platform timeline entry |
| `_Internal/Accomplishments.md` | An outcome-first entry for review time |

The `_system/` folder here holds only the config and the owner's preferences. A real vault made with `scripts/new-vault.py` also contains the full rules, workflows, templates, and scripts.
