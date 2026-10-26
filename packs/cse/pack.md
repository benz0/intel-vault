---
name: cse
title: Customer Success Engineer
description: Customer accounts with product relationships, renewals, risk, and a customer-success platform (Gainsight or similar) that the vault feeds but never writes to.
subject_dirs: [Accounts]
portfolio_dir: _Portfolio
config_keys:
  cs_platform: Gainsight      # the customer-success system of record
  crm: Salesforce             # optional, for opportunity context
  products: []                # products you cover, e.g. [Vault Enterprise, Terraform Enterprise]
  competitors: []
---

# CSE pack

For anyone who owns the technical relationship with a set of customer accounts after the sale: Customer Success Engineers, Technical Account Managers, CSMs with a technical bent.

## What it adds

| Adds | Purpose |
|---|---|
| `Accounts/{Account}/` | One folder per customer, with product relationship folders inside |
| `_Portfolio/` | Renewal Calendar, Risk Board, Internal People |
| Rules `30-customer-success.md` | Customer-success platform handling, cadences, risk model |
| Rules `35-account-structure.md` | Account folder layout, frontmatter, multi-relationship products |
| Workflow `risk` | Pressure-test an account's risk posture |
| Workflow `cs-update` (alias `gainsight`) | Draft a timeline entry, sentiment change, or CTA |
| Workflow `build-vault` | Build a full account from a folder of sources, in phases |
| `templates/account-files.md` | Templates for every account file |

## Config

Add the keys above to `_system/config.md` (the setup script does this). Your employer's specific process (risk signal names, escalation thresholds, field dropdown values) goes in `_system/local/rules/30-{employer}-process.md`, not in this pack.
