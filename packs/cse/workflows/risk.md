---
name: risk
description: Pressure-test an account's risk posture against the risk signals and the credible-plan test. Use when the owner says "is X at risk", "review risk for X", "prep me for the risk review", or "check my risk records".
aliases: [risk-review]
argument-hint: "<account>"
---

# Risk review

Assess the account honestly. The standing critique in risk reviews is "no credible plan." Find that gap before the owner's manager does.

Use the signal list in the local rules if one exists, otherwise the default list in `30-customer-success.md`.

## Signal check

For each signal, mark **Present / Weak / Missing** with evidence and its date. Be strict: a "live cadence" where the customer has no-showed twice is Weak, not Present.

## Risk classification

For each open risk, classify it **technical, consumption, or commercial** (`30-customer-success.md`). Call out any that are misfiled in the vault or in the platform.

## Credible plan test

For each open risk:

1. What specifically will change?
2. Who is doing it, by name?
3. By when, with a date?
4. How will we know it worked, measurably?
5. What happens if it does not?

**If you cannot answer all five from the vault, the plan is not credible.** Say so plainly. A review that passes an account with no plan removes the flag without removing the risk.

## Output

```markdown
# Risk Review: {Account} ({Date})

## Verdict
{One paragraph. Lead with the honest answer.}

## Signal scorecard
| Signal | Status | Evidence (dated) |

## Open risks
{Per risk: type, severity, evidence, plan credibility verdict}

## What {manager from config} will ask
{The 3-5 hardest questions, and whether the owner has an answer to each}

## Gaps to close before the review
{Ordered, each with what the owner has to do}
```

Include the "will ask" section every time. It is the most useful part.
