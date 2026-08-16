## Git & Commits — the human owns commits

Change files and **leave them in the working tree**. Making an edit is not the same as committing
it.

- Do **not** `git add` / `git commit` / `git push` as part of finishing work. Only when the human
  explicitly asks in the current request, and even then keep it surgical
  (`git add <specific paths>`, never `-A` or `.`).
- **Never** stage binary assets, generated test fixtures, or tracking-/history-altering operations
  (retiring tracked directories, large migrations or renames, `.gitignore` policy changes) on your
  own. Those always wait for the human.
- If a change is only durable once committed, escalate via
  `.agents/office-space/{{workflow}}/mail/out/`: state exactly what would be staged and let the
  human commit it. Do not delegate the commit to another agent.
- Read-only git (`status`, `diff`, `log`, `ls-files`) is always fine.
