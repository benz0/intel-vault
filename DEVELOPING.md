# Developing intel-vault

For anyone changing this repo, person or AI assistant. Read this, `README.md`, `CHANGELOG.md`, and `docs/ROADMAP.md` before the first change.

## What this repo is

A tool-neutral spec for a markdown "intel vault", plus scripts that install and update it. Users copy it into their vault as `_system/` and never edit it there except in `_system/local/` and `_system/config.md`.

| Folder | Holds | Installed to |
|---|---|---|
| `core/` | rules, workflows, templates, scripts every vault gets | `_system/` |
| `packs/{name}/` | role add-ons (`cse`, `people-manager`) | `_system/packs/{name}/` |
| `adapters/` | setup notes per AI tool | `_system/adapters/` |
| `scripts/` | `new-vault.py`, `update-vault.py`, `selftest.py` (run from the repo) | not installed |
| `docs/` | `MIGRATING.md`, `ROADMAP.md`, design notes | not installed |
| `examples/demo-vault/` | a fictional vault (Bluefin Logistics) | not installed |
| `examples/demo-inbox/` | ten fictional emails for checking the `inbox` workflow by hand (`docs/inbox-acceptance.md`) | not installed |

## House rules

1. **No em dashes** (U+2014) anywhere. Use commas, periods, or parentheses. The one exception is the signature divider string, three em dashes separated by spaces, used as an example of `forbidden_chars_allow`.
2. **Tool-neutral.** Never name a specific AI assistant in core, packs, docs, or scripts, except in its own file under `adapters/`. Write "your AI tool" or "an assistant that only reads its own rules folder". Tool-specific behavior goes behind a config key (see `export_alias_skills` for the pattern).
3. **Nothing personal or employer-specific.** No real customer names, people, figures, or internal processes. Examples use the fictional Bluefin Logistics or placeholders like Jordan Lee and Pat Smith. An owner's own rules belong in their `_system/local/`, never here.
4. **Never break a user's vault.** Scripts must not overwrite, move, or delete a user's notes. `update-vault.py` never touches `_system/local/` or `config.md`. A new config key needs a safe default when it is missing, because existing users will not have it.
5. **Credits stay as written** in the README: Eric Reeves (IBM/HashiCorp SE) and Kwadwo Eck. Do not remove or reword them.
6. **Plain Python 3, standard library only,** unless a script says otherwise (`email-to-md.py` uses `extract-msg` for `.msg` files only).

## How a change goes in

1. **Branch.** Never commit to `main`. Name it `proposed/{version}` or `proposed/{short-topic}`.
2. **Make the change.** Keep each branch to one theme.
3. **Run the self-test:** `python3 scripts/selftest.py`. Every check must pass. If you changed behavior the self-test does not cover, add a check for it.
4. **Update `CHANGELOG.md`** (new version at the top, one line per change, why it changed) and bump `VERSION` (patch for fixes, minor for new commands, packs, or config keys). A change that is only docs (nothing under `core/`, `packs/`, `adapters/`, or `scripts/` changes behavior) may instead go under an `## Unreleased` heading at the top of the changelog, with no version bump. When the next version is released, its entry absorbs the Unreleased lines.
5. **Summarize for the owner before committing:** each file changed, what changed, why, and the self-test result. Wait for an explicit yes.
6. **Commit and push the branch.** Do not merge it.
7. **Review.** A second assistant or person who did not write the change reviews the branch and reruns the self-test. Only then is it merged to `main`.
8. **Apply to a real vault** with `python3 scripts/update-vault.py <vault> --dry-run` first, then without `--dry-run`. Then check that every command the owner uses still shows up in each AI tool, not only that the files exist.

## The self-test

`scripts/selftest.py` builds throwaway vaults in a temp folder and checks install, export (and that a second export changes nothing), update, adopt, email conversion, the checker, the people-manager pack and inbox workflows, and the repo itself. It checks structure and safety text only; whether an assistant sorts mail correctly is checked by a person with `docs/inbox-acceptance.md`. It never touches a real vault.

**Banned words:** to keep a name out of the repo without writing it into the repo, list it in `.git/info/banned-words`, one per line. That file lives inside `.git/` and is never committed. Check 8b fails if any tracked file contains one.

## Where work comes from

- `docs/ROADMAP.md`: "Next", the feedback queue, and open design questions.
- Findings from real migrations and updates (the user's migration log). Each one becomes a roadmap item or a fix, with the finding quoted in the changelog line.

## Things that went wrong before (so they do not again)

- A script that reported "clean" without counting. Every check prints real numbers.
- A setting typed below the config block, where scripts cannot read it. Config notes now say where settings go.
- An update that silently removed command names a tool relied on. The exporter now keeps files whose source still exists, and the migration check asks for every old command name by name.
- A self-test that passed here and failed on the owner's machine: it only scanned files already added to git, so a new file with the forbidden character slipped through. It now scans new files too, and the test itself builds that character with `chr(0x2014)` instead of typing it.
- `cp -p` failing silently on a network share during a backup. Verify copies with `diff -rq`.
