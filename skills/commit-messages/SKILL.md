---
name: commit-messages
description: Use when writing git commit messages or staging commits.
Governs commit message format and conventions.
---

# Commit messages
Format:
<type>(<scope>): <subject>

Types:
feat, fix, refactor, style, docs, chore, test

Rules:
- Imperative mood ("add", not "added").
- Subject ≤ 60 chars, no trailing period.
- Body is optional; wraps at 72 chars; explains *why*, not *what*.
- One commit per logical change. Don't squash unrelated work.

Bad:
- "fix"
- "update"
- "WIP"
- "reformat: cleaned up the project"

Good:
- "feat(auth): add password reset endpoint"
- "fix(invoices): correct rounding on EUR totals"