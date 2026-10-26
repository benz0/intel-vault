# Data handling

This vault holds confidential material: the owner's employer's, their customers', and other people's. The `data_policy` line in `_system/config.md` summarizes what the owner's employer allows in AI tools. **That policy wins over anything here.** If it is blank, ask the owner before ingesting anything that looks sensitive.

## Never write these into any file in this vault

- **Secrets and credentials:** passwords, API keys, access tokens, private keys, certificates, `.env` contents, recovery or unseal keys.
- **Government and financial identifiers:** national ID or Social Security numbers, bank or card numbers, full customer account numbers where policy forbids them.
- **Health information** about anyone.
- **Anything the employer's AI policy prohibits.**
- **Third-party material the owner has no right to use.**

## If you encounter excluded content

Stop. Tell the owner what you found and where. Do not copy it into a vault file, do not quote it back, and do not summarize around it in a way that preserves its value. Redact and flag.

This comes up most with configuration snippets, runbooks, spreadsheets, and pasted emails, which often carry real tokens or account numbers. Check before you ingest.

## Financial figures

Contract values, balances, revenue, quota, and compensation appear in work vaults by necessity. Keep them inside vault files. Never put them in anything customer-facing, and flag it if the owner asks for an external draft that includes them.

## Named individuals

Files about people (customers, colleagues, direct reports) hold names, roles, priorities, and history.

- **Business context only.** Role, priorities, concerns, decision authority, engagement history, commitments.
- **No personal details,** no health information, no speculation about anyone's job security or private life.
- **Assessments must be evidence-based** and attributable to something the person said or did.
- **Write every note as though that person may one day read it.**
- **Performance and HR matters** about direct reports follow the employer's policy. When unsure, record that a conversation happened and where the official record lives, not the content.

## Work and personal stay separate

A work vault never holds the owner's personal, family, legal, medical, or personal-finance matters. If the owner raises one in a work session, say so out loud and do not record it here. Those belong in a separate personal vault, if the owner keeps one.

## The owner's own privacy

A work vault on an employer laptop, run through an employer's AI account, may be visible to the employer. Anything the owner would not want their employer to read (job searches, private opinions of colleagues, personal circumstances) does not belong in it.
