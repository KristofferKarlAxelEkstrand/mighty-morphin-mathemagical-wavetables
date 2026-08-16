# Controlled-language rules (full set)

Distilled from ASD-STE100 (Simplified Technical English) for general documentation use, not just
aerospace maintenance manuals. Apply **strict** mode to procedures, error messages, CLI help, and
safety-relevant copy. Apply **flavored** mode (vocabulary rules relaxed) to narrative docs.

## Word selection

- Use exactly one name for one thing throughout a document. Do not alternate `endpoint` / `URL` /
  `route` for the same concept.
- Prefer the short, common word: `start` over `begin` or `commence`, `use` over `utilize`, `help`
  over `facilitate`, `get` over `obtain`, `show` over `display` (when both mean the same thing
  here), `end` over `terminate`.
- Assign each word a single meaning in the document. If a word normally has two senses (e.g. `close`
  as verb vs. adjective), pick one and use a different word for the other sense.
- Cut marketing and hedge language: `seamless`, `powerful`, `robust`, `cutting-edge`, `effortless`,
  `simply`, `just`, `easily`. These add no checkable content.
- American spelling, for consistency with the rest of this repo's docs.

## Verb discipline

- Write in active voice: subject performs the action. "The linter reports violations," not
  "violations are reported by the linter." Passive voice is acceptable only when the actor is truly
  unknown or irrelevant.
- Use a verb for an action instead of a noun. Say "analyze the input," not "perform an analysis of
  the input." Say "the tool validates the file," not "the tool performs validation."
- Avoid stacked auxiliaries ("should be able to be configured to..."). State the fact plainly.
- Prefer simple tense over "-ing" forms where either works: "the script checks the file," not "the
  script is checking the file," unless the ongoing aspect is the point.

## Sentence and paragraph structure

- Procedural/instruction sentences: 20 words or fewer.
- Descriptive sentences: 25 words or fewer.
- One instruction per sentence. Do not chain two commands with "and" or "then."
- One topic per paragraph, six sentences or fewer.
- State the condition before the command: "If the config file is missing, create it," not "Create
  the config file if it is missing." Readers act faster on a condition they see first.
- Steps in a procedure: imperative mood, numbered list, one action per step.

## Punctuation

- No semicolons — split into two sentences instead.
- No contractions in strict-mode copy (errors, CLI help, procedures). Flavored mode may use them
  where the surrounding prose already does.
- Em dashes are fine for a genuine aside. Do not use them to avoid deciding where a sentence ends.
- Use articles (`a`, `an`, `the`, `this`, `these`) — omitting them to sound terse reads as broken,
  not concise.

## Organization

- Numbered vertical lists for procedures and sequential steps. Bulleted lists for unordered facts.
- Put the most important fact first in a paragraph, not buried in the third sentence.
- Name the file/command/flag exactly as it appears in the system — do not paraphrase identifiers.

## Strict vs. flavored mode

|                           | Strict                                             | Flavored                                         |
| ------------------------- | -------------------------------------------------- | ------------------------------------------------ |
| Applies to                | Procedures, errors, CLI help, safety copy          | READMEs' prose, design rationale, narrative docs |
| Vocabulary lockdown       | Yes — one word, one meaning, short-word preference | Relaxed — natural vocabulary is fine             |
| Sentence/paragraph limits | Yes, strictly                                      | Yes — these rules do not change by mode          |
| Active voice              | Yes                                                | Yes                                              |
| Contractions              | No                                                 | Acceptable if consistent with surrounding prose  |

Flavored mode still bans marketing language and still requires verified accuracy — only the
vocabulary constraint relaxes.
