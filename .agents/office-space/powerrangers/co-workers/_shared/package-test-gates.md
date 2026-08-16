## Project verification gates

The host repository decides how changes are verified. Treat its `WORKFLOW.md`, task acceptance
criteria, and configured `space.json` `review.machineChecks` as the authority.

Do not invent commands merely because another project uses them.

### Evidence ladder

Define the project's real ladder in `WORKFLOW.md`: the narrow check used while editing, the normal
handoff gate, any integration or packaging gate, and any human-controlled release gate. If tasks use
`verification_tier`, the workflow must define every supported value and the evidence required for
each one. Implementers never rewrite a task's tier downward.

1. **Implementers → review:** run the narrowest available check that exercises the changed behavior,
   then the broader handoff check required by the host.
2. **Reviewers:** confirm that the named commands exist in this repository, cover the submitted
   paths, and produced the reported result.
3. **QA:** follow the host's configured evidence tier and reuse policy.
4. Run integration, packaging, deployment, or release checks only when the host policy or task
   requires them. Do not silently substitute a cheaper command for a required gate.
5. Before starting a long or shared check, determine whether the host provides a lock, concurrency
   limit, or fresh-result reuse policy. Follow it exactly.
6. After a gate rejection, use the cheapest checks that cover the listed fixes until the hand-back
   that claims the full gate is ready.
7. Report the exact commands run and their results. If a required command is unavailable or the host
   has no evidence policy, stop and ask the lead to configure one rather than guessing.

### Machine review

Greenfield `space.json` configures only the `workflow-integrity` machine check
(`office-space check`) as a portable baseline. Add project-specific test, lint, build, or package
commands to `review.machineChecks` before relying on machine review for those properties.
