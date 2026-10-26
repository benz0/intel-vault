# Account file templates

Every file also gets frontmatter (`35-account-structure.md`) and the standard footer (`40-vault-conventions.md`).

---

## Account Overview.md

```markdown
> Sources span YYYY-MM-DD to YYYY-MM-DD. Today is YYYY-MM-DD.

# Account Summary
- Industry
- Headquarters
- Current Products
- Overall Status
- Executive Summary

# Current State
- Environment
- Product Relationships
- Competitors
- Renewal Status

# Open Questions

# Executive Takeaway
One paragraph suitable for leadership.
```

---

## Customer Intelligence Dashboard.md

```markdown
> Sources span YYYY-MM-DD to YYYY-MM-DD. Today is YYYY-MM-DD.

# At a glance
| Product | Renewal | ACV | Sentiment | Primary risk |

# What the customer is trying to do

# Who matters
(Champion, economic buyer, executive sponsor, detractors. Link stakeholder files.)

# What changed recently

# What we do not know
```

---

## Stakeholder file

```markdown
---
type: stakeholder
organization:
relationship:
influence:
champion:
economic_buyer:
health:
last_updated:
---

# Name
## Title
## Products
## Role
## Influence
## Relationship Status
## Priorities
## Concerns
## Current Initiatives
## Notes
## Key Quotes
## Related Meetings
```

`Stakeholder Index.md` is a compact table with sections for Customer Stakeholders, Internal Stakeholders, Champions, Economic Buyers, and "Seen once, role unknown."

---

## Product and competitor files

Path: `Accounts/{Account}/{Product}/{Name}.md`. Competitors live with the product they threaten.

```markdown
# Status
# Adoption
# Use Cases
# Stakeholders
# Risks
# Opportunities
# Related Meetings
```

---

## MEDDPICC.md

One per product relationship.

```markdown
# Metrics
# Economic Buyer
# Decision Criteria
# Decision Process
# Paper Process
# Identify Pain
# Champion
# Competition
# Overall Assessment
```

Each section carries **Current Status / Evidence / Known Gaps / Confidence Level.**

---

## Account Plan.md

```markdown
# Relationship Summary
# Executive Summary
# Current State
# Customer Goals
# Our Objectives
# Strategic Objectives
# Opportunities
# Risks
# Success Criteria
# Next Steps
# Account Assessment
```

---

## Success Plan.md

```markdown
# Executive Summary
# Customer Goals
# Our Goals
# Step-by-Step Plan
# Current Workstreams
# Risks To Success
# Opportunities
# Success Metrics
# Next Use Case (what, when, expected consumption)
# Next 90 Days
# Assessment
```

---

## Architecture.md

```markdown
# Current State
# Future State
# Identity Model
# Cloud Platforms
# Governance Architecture
# Operational Considerations
# Risks
# Opportunities
# Assessment
```

---

## Risks and Opportunities.md

Per risk:

```markdown
## {Risk Name}
Type: technical | consumption | commercial
Status:
Severity:
Probability:
Impact:
Description:
Mitigation:
Owner:
Stakeholders:
Related platform record:
```

Per opportunity:

```markdown
## {Opportunity Name}
Value:
Likelihood:
Status:
Description:
Next Steps:
```

---

## Action Tracker.md

```markdown
# Open Customer Actions
- [ ]

# Open Internal Actions
- [ ]

# Risks Being Tracked

# Opportunities Being Tracked

# Completed Actions
- [x]

# Next Executive Review Topics
```

Every open action carries an owner and a date. The owner's own commitments also go on the vault task list.

---

## Account meeting file

```markdown
---
type: meeting
date:
account:
product:
attendees:
source:
---

# Meeting Summary
(2-5 paragraphs)

# Customer Action Items
# Internal Action Items
# MEDDPICC Changes
# Stakeholder Updates
# Product Adoption Updates
# Risks Identified
# Opportunities Identified
# Strategy Changes
# Key Quotes
# Executive Takeaways
```

---

## Meeting Log.md

Chronological, every meeting. Columns: Date, Name, Product, Outcome, Stakeholders, Summary. Every row links to its meeting file or, for log-only meetings, its source.

---

## _Portfolio files

**Renewal Calendar.md:** table of Account, Product or relationship, Renewal date, ACV, Sentiment, Risk status, Plan credible Y/N. Sorted by date.

**Risk Board.md:** table of Account, Risk, Type, Severity, Platform record, Recovery plan Y/N, Owner, Next check. Note that the owner tracks risks they do not own; the Owner column says who acts.

**Internal People.md:** colleagues across accounts (AEs, SEs, managers, support), one row each with role and accounts.
