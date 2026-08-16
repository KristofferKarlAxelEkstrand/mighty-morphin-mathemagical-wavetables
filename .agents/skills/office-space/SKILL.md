---
name: office-space
description:
  Guidelines and design tips for designing effective autonomous agents and co-workers in the
  office-space ecosystem.
---

# Designing an Effective Workforce

The `office-space` tool allows you to orchestrate an entire team of autonomous agents. The technical
configuration of each agent is crucial, but equally important is how you design their roles,
boundaries, and communication patterns. Here are key tips for making really good co-workers and
getting an effective workforce.

**Lifecycle (not covered here):** first-run order, keep/refresh after package bumps, and drift
checks → skill `office-space-onboard`. Mission, lineup, pipeline, and human gates for _this_ host →
skill `office-space-team-design`. Day-to-day mail/tasks/slack → skill `office-space-protocol`. Do
not paste those bodies into this tips skill; open them when you need the full sequence.

## 1. Role Clarity and Narrow Scopes

A common mistake is designing "god agents" that do everything. The most effective workforce is
composed of specialists.

- **Narrow their focus:** Instead of one "Developer" agent, have a "Frontend Developer", a "Backend
  Developer", and a "Database Optimizer".
- **Limit their context:** Only provide agents with the context they need for their specific role.
  The `quality` agent doesn't need to know how the design system was brainstormed; they only need
  the technical spec and the PR diff.
- **Explicit responsibilities:** In the agent's prompt (`.prompt.md`), state explicitly what they
  _are_ and _are not_ responsible for. (e.g. "You are the `tests` agent. You NEVER write feature
  code. You only write and execute tests.")

## 2. Strong Boundaries and Gates

Agents left to their own devices can overwrite each other's work or drift from the objective.

- **Use the `review` stage:** Never let an implementer merge code directly. Always enforce that
  tasks must transition to the `review` stage, requiring a separate `quality` agent to verify the
  work against the spec.
- **Enforce Owned Paths:** Leverage the `owned_paths` lock. When an agent claims a task, ensure they
  lock the specific directories they are working on. This prevents race conditions and merge
  conflicts between concurrent agents.
- **Machine Gates:** Use `machine-review.js` for low-risk tasks to ensure basic formatting, linting,
  and tests pass before a human or high-level `quality` agent spends time on it.

## 3. Communication Discipline

Agent-to-agent communication can quickly devolve into noisy, unhelpful chatter.

- **Prefer Async State over Chat:** Agents should communicate through the task board (`tasks/todo`,
  `tasks/working-on`) and structured messages (`mail/in`, `slack/`) rather than unstructured chat.
- **Terse and Actionable:** Instruct agents (in their shared partials) to lead with the result or
  blocker. Cut out greetings and ceremony. Every message should contain exactly what the recipient
  needs to act on next.
- **Handoffs:** When a task moves stages (e.g. from `implementing` to `qa`), ensure the handoff
  message includes a link to the task file, the specific commit or diff to review, and the expected
  outcome.

## 4. Bounded Memory

An agent that remembers everything will eventually become too expensive and slow to operate.

- **Use `memory-log.js`:** Ensure your agents use the memory log to append findings.
- **Rely on Compaction:** The system automatically compacts older entries into single-line digests.
  Teach agents to trust the digest and only dig into recent entries for immediate context.
- **Durable Records:** If an agent learns a rule that applies permanently (e.g. "We always use
  snake_case for database columns"), instruct them to write it to a durable `records/decisions/`
  file rather than keeping it in their transient memory.

## 5. The Team Lead Bottleneck

The Team Lead is the router for your workforce. If they fail, the team stalls.

- **Keep the Lead Fast:** The Team Lead should focus exclusively on triaging `mail/in/`, breaking
  down epics into smaller tasks in `tasks/todo/`, and unblocking agents.
- **No Implementation:** The Team Lead should never write code. If they do, they aren't leading.
- **Clear Delegation:** Give the Team Lead explicit instructions on which tasks go to which roles.

## Summary Checklist for a Good Co-Worker

1. [ ] Has a specific, narrow role.
2. [ ] Uses `task-transition.js` to claim work and lock paths safely.
3. [ ] Sends structured, concise messages via `mail/` or `slack/`.
4. [ ] Uses `memory-log.js` to remember cross-turn context.
5. [ ] Submits work to a reviewer instead of self-approving.

## Sibling skills

| Skill                      | Use for                                        |
| -------------------------- | ---------------------------------------------- |
| `office-space-onboard`     | After init / keep current / drift checklist    |
| `office-space-team-design` | Redesign roles, WORKFLOW, gates, first backlog |
| `office-space-protocol`    | mail / tasks / slack / memory runtime          |
