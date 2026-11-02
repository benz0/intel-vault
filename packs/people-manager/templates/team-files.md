# Team file templates

Every file also gets frontmatter and the standard footer (`40-vault-conventions.md`). Everything here is work only. The hard boundary in `30-people-management.md` applies to every field.

---

## Team/{Name}/Current State.md

```markdown
---
type: team-member-state
person: {Firstname Lastname}
role:
last_one_on_one: YYYY-MM-DD
last_updated: YYYY-MM-DD
---

# {Firstname Lastname} Current State

> Work only. Newest first. Nothing HR-related, personal, or about other team members.

## Status notes

**{Firstname Lastname} notes (YYYY-MM-DD, topic):** Source: [[{path to source}|{short name}]]
- ...

## What they own
- ...

## Open requests from them
- ...

---
*Last updated: YYYY-MM-DD | Sources: [[...]] | Confidence: High/Medium/Low*
```

---

## Team/{Name}/1-1s/YYYY-MM-DD {Name} 1on1.md

```markdown
---
type: one-on-one
person: {Firstname Lastname}
date: YYYY-MM-DD
source: "[[...]]"
---

# 1:1 with {Firstname Lastname}, YYYY-MM-DD

## Discussed
(Work topics only.)

## Decided

## I committed to
(Each also goes to the task list with this note as its source.)

## They committed to
(Each also goes under Waiting on others.)

## Added to their retrain list

## Skipped under the boundary
(A number only, or leave blank. No detail.)
```

---

## Team/{Name}/Retrain List.md

```markdown
---
type: retrain-list
person: {Firstname Lastname}
last_updated: YYYY-MM-DD
---

# {Firstname Lastname} Retrain List

> Skills and steps to refresh. State each item as the process, not the person's failing. Close items; do not delete them.

## Open

- [ ] **{Process or skill to refresh}.** Raised YYYY-MM-DD. `Source: {meeting or email file}, YYYY-MM-DD`

## Closed

- [x] **{Item}.** Raised YYYY-MM-DD, closed YYYY-MM-DD ({how it was closed}).
```
