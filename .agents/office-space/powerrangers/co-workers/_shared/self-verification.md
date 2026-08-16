## Self-Verification Loop

Verify your own work before reporting it:

1. For each unit of change, run the narrowest relevant check (a focused test, a linter, a build of
   just the affected target) before moving on. Do not wait until the whole task is "done" to find
   out something broke three edits ago.
2. At task handoff, run the broader check your project defines for that gate. Prefer a **fast
   default suite** when the project provides one; run **heavier integration / full verify** only
   when the workflow says so (see **package-test-gates** / host WORKFLOW evidence ladder when
   present), not on every tiny edit.
3. If a check fails because of your change, fix it and retry, up to a **few** attempts. If the same
   failure is already recorded against this source state, reference that instead of repeating the
   run.
4. Only after repeated failed attempts, or on a genuine architectural blocker, escalate with a
   `blocked` message.

**Trap:** confirm the command you ran actually exercises the code you changed — a lint-only or
type-check-only command is not test evidence, even when its name suggests otherwise. Name the exact
command(s) in the handoff.

Report what actually happened. If checks fail, say so and include the output. If you skipped a step,
say that. Never report work as verified that you did not verify.
