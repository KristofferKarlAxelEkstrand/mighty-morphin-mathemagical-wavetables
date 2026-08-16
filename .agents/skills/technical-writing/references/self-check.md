# Pre-submit self-check

Run through this list before moving a docs draft to `review`. Fix what you find, then re-check — do
not submit on the first pass.

- [ ] No sentence over 20 words (procedures/instructions) or 25 words (descriptions).
- [ ] No semicolons.
- [ ] No contractions in strict-mode copy (errors, CLI help, procedures).
- [ ] No passive voice where the actor is known and nameable.
- [ ] No nominalizations (`perform an analysis`, `make a determination`) where a verb would do.
- [ ] One name per concept — grep the draft for known synonyms of the same thing.
- [ ] No paragraph over six sentences.
- [ ] No marketing/hedge words (`seamless`, `powerful`, `robust`, `cutting-edge`, `effortless`,
      `simply`, `just`).
- [ ] Every command, flag, and path in the draft has been run or read from the source — not assumed.
- [ ] Conditions come before commands, not after.

Optional machine check: `node .agents/skills/technical-writing/scripts/lint.js <file>` scores the
mechanical subset of this list — length, semicolons, contractions, passive voice, nominalizations,
paragraph length, marketing words. It cannot check terminology consistency or factual accuracy — do
those two by hand.
