---
name: technical-writing
description: >-
  Write and review manuals, READMEs, guides, CLI help text, error messages, and in-repo agent docs
  using controlled-language rules distilled from ASD-STE100 (Simplified Technical English). Use when
  drafting or editing documentation, a manual, a README, help/usage text, an error message, or when
  asked to cut verbosity or "AI slop" out of written prose.
---

# Technical Writing

Controlled language beats natural-language sprawl for instructions: fewer legal readings, less room
for "sounds right but is ambiguous." Apply these rules to prose deliverables. They are a style
discipline, not a grammar cage.

## Do this

1. **One name per thing.** Never vary terminology for the same concept across a document.
2. **Short, common words.** `start` not `begin`, `use` not `utilize`, `help` not `facilitate`, `get`
   not `obtain`. One word, one meaning — do not let a word cover two senses.
3. **Active voice, real verbs.** "The parser reads the file," not "the file is read by the parser."
   Avoid nominalizations (`perform an analysis` → `analyze`).
4. **Imperative for steps.** State the condition before the command: "If the file is missing, create
   it" — not the reverse. One instruction per sentence, one topic per paragraph.
5. **Hold the line, hold the shape.** ≤20 words for procedural/instruction sentences, ≤25 for
   descriptive ones. ≤6 sentences per paragraph. No semicolons — split into two sentences. No
   contractions in strict copy (error messages, CLI help, procedures).
6. **Cut marketing words.** `seamless`, `powerful`, `robust`, `cutting-edge`, `effortless` carry no
   checkable meaning — say what the thing actually does.
7. **Verify before you publish.** Run every command/flag/path you document. Docs that describe
   behavior the product does not have are worse than no docs.

Two modes:

- **Strict** — procedures, error messages, CLI help, safety-relevant copy. Apply every rule above,
  including the word-choice constraints.
- **Flavored** — narrative docs, design rationale, READMEs' prose sections. Keep sentence/paragraph
  discipline and active voice. Relax the vocabulary lockdown — a narrative can say "straightforward"
  even though a procedure should not.

## Load when

| File                                                                               | Open when                                                                       |
| ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| [references/controlled-language-rules.md](references/controlled-language-rules.md) | Writing longer or more formal docs and you need the full rule set with examples |
| [references/self-check.md](references/self-check.md)                               | Before submitting a draft — the pre-publish checklist                           |
| [references/sources.md](references/sources.md)                                     | You want the rationale/evidence behind these rules, or need to cite them        |
| `scripts/lint.js`                                                                  | You want a machine check for violation density before handing off a draft       |

## Gotchas

- This is a **style** discipline, not a spec for every sentence you write. Do not apply strict-mode
  vocabulary lockdown to prose that is not procedural (see Flavored mode above).
- `scripts/lint.js` is advisory: it flags candidates for a human/agent read, it does not decide
  correctness. A clean report does not mean the docs are accurate — verify commands and behavior
  separately.
- Longer sentences are sometimes genuinely clearer than two choppy ones. Treat the length ceiling as
  a trigger to re-read the sentence, not an automatic split.
