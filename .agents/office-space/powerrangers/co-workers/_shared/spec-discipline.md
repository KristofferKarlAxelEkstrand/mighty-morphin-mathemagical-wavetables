## Specs Are the Truth

Specs for this workflow live in `spec/` — see `spec/README.md` for the index. Read the spec that
covers your task **before** starting it; check your work against it before reporting.

- Only `approved` specs are binding.
- If you think a spec is wrong, propose the change in your report — do not edit its verdict/status
  yourself. Specs are owned by whoever your workflow designates (often the team lead), not by
  whoever is implementing against them.
- Quality bars and acceptance criteria for each pipeline stage belong in your workflow's mission doc
  (`.agents/office-space/{{workflow}}/WORKFLOW.md` or similar) — read it once, then treat it as
  binding.

**If the code contradicts its spec's stated intent, stop.** That is a defect in one of them, and
which one changes is a design decision for the spec owner (or the human), not yours. Say so in a
`blocked` message naming the spec section and the file:line that disagrees. Never quietly pick a
winner.
