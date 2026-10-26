# Customer success platform and process

The customer-success platform named in `cs_platform` (Gainsight by default) is the system of record that leadership reviews. This vault feeds it. It does not replace it.

Your employer's specifics (exact field values, signal names, escalation thresholds, who approves what) belong in `_system/local/rules/30-{employer}-process.md`. Where that file and this one disagree, the local file wins.

## Hard rule

**Never log an activity, update a field, close a CTA, or submit anything in the platform without the owner's explicit yes for that action.** Draft it, show it, wait. Assume there is no direct integration unless the owner says otherwise; everything goes through their hands.

## The governing principle

> If it isn't in the timeline, it didn't happen.

If a vault file records something material that is not in the platform yet, flag it as an open action on the task list.

## Default update cadences

Replace these in your local rules with your organization's actual cadences.

| Item | Cadence |
|---|---|
| Use cases | Monthly |
| Consumption | Monthly |
| Escalated or program accounts | Weekly |
| Success plans | Every 6 months |
| Health checks | Every 6 months |

| Sentiment | Update frequency |
|---|---|
| Red | Weekly |
| Yellow | Every 2 weeks |
| Green | Monthly |

## Timeline entry content

Every meeting summary for the platform includes:

1. Key goals and objectives
2. Main discussion points
3. Risks and blockers
4. Follow-up items with named owners
5. Next steps for both parties

Lead the headline with **date and the owner's initials** (`owner_initials` in config). That is what reviewers read first.

## Risk classification

Every risk gets one root-cause type. Getting it wrong sends it to the wrong owner.

| Type | Means | Usually owned by |
|---|---|---|
| **Technical** | The product is not working, not deployed, or not adopted for technical reasons | The CSE |
| **Consumption** | Bought but not used enough to justify the renewal | CSE with a recovery plan |
| **Commercial** | Price, contract, budget, competitor, relationship with sales | Sales leadership |

**Misfiled risks are a recurring problem.** A pricing objection filed as a technical risk lands on the wrong desk. Call it out when you see it.

Close a risk record when the account is no longer at risk. Stale open risks distort every portfolio view.

## Default risk signals

A relationship is healthier when each of these is present. Replace with your organization's model in local rules.

| Signal | Present when |
|---|---|
| Scope owner | A named customer person owns the technical scope |
| Outcome owner | A named person is accountable for the business outcome |
| Live cadence | A recurring meeting exists **and is actually happening** |
| Success plan | One exists and was updated within 6 months |
| Consumption health | Consumption is healthy, or a recovery plan is in place |
| Dated next action | The platform shows a next action with a date |

## Success plan naming

Default: `[Customer] [Product] Success Plan [Year]`, due date equal to the renewal date. Override in local rules.
