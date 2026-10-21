---
name: doc-writer
description: Use when writing or updating documentation — README sections, 
inline docstrings, or standalone guides. Governs voice, structure, and what to include.
---

# Documentation

Voice:
- Direct. "Run `npm install`" not "You may wish to run `npm install`."
- Plain English. No marketing language ("powerful", "robust", "seamless", "cutting-edge", "AI-powered").
- Second person ("you") for guides; imperative for instructions.

Structure for any "how to" section:
1. One-sentence what-it-does.
2. Minimum viable example (copy-pasteable).
3. The two or three knobs the reader will actually turn.
4. Where to go for more.

For docstrings:
- One-line summary first. End with a period.
- Blank line, then the longer explanation if any.
- Document parameters, return values, and exceptions only when they aren't obvious from the signature.

Avoid:
- Restating what the code already shows ("This function takes x and returns y").
- Documenting every parameter with "the X parameter is the X."
- Marketing-style intros before getting to the actual instructions.