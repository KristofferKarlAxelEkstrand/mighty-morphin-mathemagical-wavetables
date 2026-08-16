# Sources and rationale

Why these rules, not invented taste:

- **EWD667** — Edsger Dijkstra, "On the foolishness of 'natural language programming'"
  (<https://www.cs.utexas.edu/~EWD/transcriptions/EWD06xx/EWD667.html>). Dijkstra argues that
  formal, constrained language rules out ambiguity that natural language lets pass unnoticed. A
  narrow, well-defined interface costs less total effort than a loose "natural" one that looks
  easier but hides interpretation gaps. That is the rationale for a controlled vocabulary and fixed
  sentence shapes over "write naturally."

- **ASD-STE100** (<https://www.asd-ste100.org/>) — Simplified Technical English, a controlled
  natural language standard built for aircraft maintenance manuals so non-native English readers get
  one unambiguous reading per instruction. `references/controlled-language-rules.md` distills its
  approach — one word one meaning, short words, active voice, sentence/paragraph limits, numbered
  procedures — for general documentation, not just aerospace manuals.

- **`woosal1337/blog`, ep01 "the cure for AI slop"**
  (<https://github.com/woosal1337/blog/tree/main/videos/ep01-the-cure-for-ai-slop>) — an experiment
  comparing writing-constraint systems on Claude and GPT-5.5 across six writing tasks. An
  STE-distilled skill cut violation density (per 100 words) by 74% on Claude and 50% on GPT-5.5. A
  plain banned-word list only managed −3% to −40%. That gap is the evidence for a full
  controlled-language system over a word blocklist, and the reason this skill ships a rule set plus
  a linter instead of just a banned-words check.

- **HN discussion of the above** (<https://news.ycombinator.com/item?id=49114639>) — useful
  counterpoints kept in mind while writing this skill. STE-style instructions can drift over a long
  session without a re-check step, hence `references/self-check.md` and `scripts/lint.js` as a
  concrete re-check, not a one-time prompt. Orwell's writing rules are a lighter-weight competing
  approach worth knowing about. This skill standardizes on ASD-STE100 because it has
  sentence/paragraph limits precise enough to machine-check.
