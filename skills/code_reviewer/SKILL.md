---
name: code-reviewer
description: Use when reviewing a pull request, a code diff, or a proposed code change. Provides a checklist of what to look for and guidance on phrasing feedback.
---

# Code review
When reviewing a diff, check (in this order):

1. **Correctness.** Does it do what the description says? Are the edge cases handled? Are there obvious bugs?

2. **Tests.** Are new branches covered? Do existing tests still pass? Are the tests testing the right thing, or just the implementation?

3. **Hallucinated APIs.** Does every imported function actually exist? Do the function signatures match? (LLM-written code drops phantom imports more often than humans do.)

4. **Over-engineering.** Are there abstractions that aren't paying for themselves yet? Configuration that nothing configures?

5. **Style.** Does it match the repo's conventions? (Naming, file organization, error handling, comment style.)

6. **Security.** Any input that crosses a trust boundary unvalidated? Any secrets in code or logs?

How to phrase feedback:
- Lead with the most important issue, not the easiest one to spot.
- Distinguish blocking comments from suggestions. Use "blocking:" or "nit:" prefixes.
- Suggest concrete alternatives, not just "this is wrong."
- Praise good choices that aren't obvious — short reviews are fine, silent reviews aren't.

Avoid:
- Generic "looks good to me" comments.
- Bikeshedding (debating one-word naming for an hour).
- Restating what the diff already shows ("you added a function").