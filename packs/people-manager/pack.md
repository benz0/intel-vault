---
name: people-manager
title: People manager
description: A supervisor's vault. A folder per direct report with 1:1 notes and a retrain list, email triage buckets for escalation requests and retraining, and a hard boundary against HR and personal matters.
subject_dirs: [Team]
config_keys:
  report_term: direct report   # what you call the people who report to you
  one_on_one_days: 14          # target days between 1:1s with each person
  escalation_chain: []         # who escalation requests go to, in order, e.g. [Pat Smith, Sam Rivera]
---

# People-manager pack

For anyone who supervises a team: a supervisor, team lead, or manager who meets each person one-on-one, collects items the team must be retrained on, and fields escalation requests.

This is the first phase. It adds the folder layout, the safety boundary, the inbox buckets, and the retrain routing. 1:1 prep, the weekly brief's "not met in a while" check, and review-cycle defaults come later (see `docs/ROADMAP.md`).

## What it adds

| Adds | Purpose |
|---|---|
| `Team/{Name}/` | One folder per person on your team, with `Current State.md`, `1-1s/`, and `Retrain List.md` |
| Rules `30-people-management.md` | The hard boundary on HR and personal content, the team layout, retrain routing, and the extra inbox buckets |
| `templates/team-files.md` | Templates for the three files above |

## Suggested `data_policy`

Add this to `data_policy` in `_system/config.md`, then add whatever your employer's AI policy says on top of it. If the policy is silent on a kind of data, silence is not permission: ask before ingesting it.

> Nothing HR-related or personal about team members.

The rule file enforces this whatever `data_policy` says. The line is there so the owner, and any assistant reading config, sees it first.

## Config

Add the keys above to `_system/config.md` (the setup script does this).

- `report_term` is the words the assistant uses for the people on your team.
- `one_on_one_days` is the gap after which a person counts as overdue for a 1:1. Nothing uses it yet; the next phase's `brief` will.
- `escalation_chain` is the people an escalation request goes to, in order. Leave it empty if you do not escalate.

Your organization's own process (what counts as an escalation, how retraining is tracked) goes in `_system/local/rules/`, not in this pack. Local rules can add to this pack but cannot loosen its hard boundary.
