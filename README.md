# intel-vault

A portable intelligence-tracking system: a folder of plain markdown files that is your system of record for the people, accounts, and work you track, plus a spec that any AI assistant can follow to keep it current.

- **Agnostic of the AI.** The rules live in the vault as markdown, not in one tool's memory. Claude, IBM Bob, Copilot, or a plain chat window can all work the same vault. Switch tools and nothing is lost.
- **Agnostic of the job.** A small core handles sessions, one task list, sources, meetings, people, and your accomplishments. **Packs** add what a role needs (accounts and renewals for customer success, a team for people managers).
- **Built for real work.** It came out of months of daily use by a Customer Success Engineer, and every rule exists because something went wrong without it.

> **Status: v0.1.** Core, the CSE pack, and the Claude and Bob adapters are in. SE, people-manager, and personal-life packs are next. See [ROADMAP](docs/ROADMAP.md).

---

## How it works

```
your-vault/
├── AGENTS.md            what's in flight right now (every AI reads this first)
├── Open Actions.md      your one and only task list
├── _Sessions/           a log per working session, so the next one can resume
├── _Internal/           your own work: 1:1s, accomplishments, praise received
├── Accounts/            subjects you track (folder names come from the pack)
└── _system/             the spec: rules, workflows, templates, scripts
    ├── rules/           how every AI must behave here
    ├── workflows/       resume, wrap, intake, prep, brief, internal, review-prep
    ├── packs/cse/       role-specific rules and workflows
    ├── local/           YOUR rules and workflows (never overwritten by updates)
    └── config.md        who you are, your timezone, where things live
```

**The daily rhythm:**

| Say | When | What happens |
|---|---|---|
| `resume` | Start of a session | Reads the last 3 session summaries and your task list, tells you what's in flight and overdue |
| `intake Acme` | After a meeting | Saves the raw transcript, writes the meeting record, shows what changed, waits for your OK, then updates everything it touches |
| `prep Acme QBR` | Before a meeting | A one-page brief: the one thing, who's in the room, what you owe, landmines |
| `wrap` | End of a session | Writes the session log, proposes task-list and status updates, asks what belongs in your accomplishments |
| `brief` | Weekly | What needs a decision, what's overdue, what's gone quiet |
| `internal 1-1` | After a 1:1 | Logs it, captures your commitments and any praise |
| `review-prep FY26` | Review season | Assembles evidence from your accomplishments log |

No command is required. Plain language works; commands load a specific checklist.

---

## Quickstart

**Needs:** Python 3 (built into macOS and most Linux; on Windows install from python.org) and an AI tool that can read your vault folder.

```bash
git clone https://github.com/benz0/intel-vault.git
cd intel-vault

# Customer Success Engineer, using Claude and IBM Bob, with an em dash ban
python3 scripts/new-vault.py ~/intel-vault-work --packs cse \
  --owner "Jordan Lee" --initials JL --role "Customer Success Engineer" \
  --org "Example Co" --manager "Pat Smith" --tz America/New_York \
  --agents claude,bob --no-em-dash
```

Then:

1. **Fill in** `_system/config.md` (especially `data_policy`) and `_system/local/rules/10-owner.md` (your writing style, signature, vocabulary).
2. **Connect your AI:**
   - **Claude:** add the skill in `_system/adapters/claude/intel-vault/` to Claude, and attach only the vault folder.
   - **IBM Bob:** run `python3 _system/scripts/sync-bob.py`, then open the vault folder in Bob. See `adapters/bob/README.md`.
   - **Anything else:** see [adapters/any-llm.md](adapters/any-llm.md).
3. Say **`resume`**.

### Updating

```bash
cd intel-vault && git pull
python3 scripts/update-vault.py ~/intel-vault-work            # add --dry-run to preview
```

Updates replace core and pack files in `_system/`. They never touch `_system/config.md`, `_system/local/`, or your notes.

---

## Packs

| Pack | For | Status |
|---|---|---|
| `cse` | Customer Success Engineers, TAMs: accounts, product relationships, renewals, risk, a customer-success platform the vault feeds but never writes to | v0.1 |
| `se` | Sales/Solutions Engineers: opportunities, MEDDPICC, CRM updates drafted for you to paste | Planned |
| `people-manager` | Supervisors: direct reports, 1:1s, team metrics, accounts you assist on | Planned |
| `personal-life` | Home, family admin, finances, a personal task list kept separate from work | Planned |

A pack is a folder with `pack.md`, `rules/`, `workflows/`, and `templates/`. Copy `packs/cse` to start a new one.

---

## Customizing without forking

Put anything specific to you or your employer in `_system/local/`:

- `local/rules/10-owner.md`: your style, signature, vocabulary
- `local/rules/30-{employer}-process.md`: your organization's actual process (risk model, field values, approval chain)
- `local/workflows/{name}.md`: replaces a core or pack workflow of the same name, or adds a new command

Local always wins, and updates never overwrite it.

---

## Hygiene

```bash
python3 _system/scripts/check-vault.py            # whole vault
python3 _system/scripts/check-vault.py Accounts/Acme
```

Counts forbidden characters, broken wikilinks, ambiguous bare links, and likely alias mismatches. AI tools report "clean" when it isn't; this gives you a number.

`_system/scripts/sheet-to-md.py` converts a spreadsheet into a disposable markdown cache (needs `openpyxl` for .xlsx).

---

## Privacy

- **Keep this repo free of real data.** It holds the spec only. Your vault is a separate folder.
- **A work vault on an employer laptop, run through an employer's AI account, may be visible to your employer.** Keep personal matters out of it.
- **Check your employer's AI policy** before putting customer or employee data in any AI tool, and record the short version in `data_policy`.

## Credits

Account file templates adapted from Kwadwo Eck's account management assistant prompt. The session-memory loop is adapted from the Claude Code + Obsidian pattern shared on r/ClaudeAI.
