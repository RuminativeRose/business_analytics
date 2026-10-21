---
name: test-scaffolder
description: Use when writing new tests for a function or module.
Governs test structure, naming, and coverage expectations.
---

# Test scaffolding

For every new function, the test file should include at minimum:
1. **Two happy-path tests** — the obvious common cases.
2. **One boundary test** — empty input, zero, max length, etc.
3. **One null / missing test** — what happens when something isn't there.
4. **One "weird real-world" test** — whatever the domain throws at you (international, malformed, mixed types).

Naming:
- Test names describe the behavior, not the implementation.
- Pattern: `test_<what_happens>_when_<condition>`.
- Bad: `test_foo_1`, `test_helper`, `test_works`.
- Good: `test_returns_none_when_input_is_empty`, `test_raises_on_unmatched_quote`.

Structure:
- One assertion per test, where possible.
- Arrange / Act / Assert with a blank line between sections.
- No I/O, no network, no time.sleep. If the function under test does I/O, inject the dependency.

Avoid:
- Tests that test the mock instead of the behavior.
- "Test scaffolding" tests that just import the module and assert True.
- Long shared fixtures that obscure what each test is actually checking.