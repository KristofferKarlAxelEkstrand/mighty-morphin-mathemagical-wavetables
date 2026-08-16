---
id: e001
title: Generator audio contract for every registered generator
status: todo
created: 2026-08-15
---

# E001 — Generator audio contract

Make tests and generators match spec `S001`. Today `any_generator` is the first registry entry
only. `test_advanced.py` allows DC `< 0.8` and peak in `0.8–1.2`. `test_edge_cases` calls
`generate` with `u=-10` and does not expect `ValueError`.

## Tasks

- T002 — Parametrize existing quality tests over all registered generators (no tighter numbers)
- T003 — Tighten assertions to S001
- T004 — Fix generators that fail T003

## Done

Every name in `get_registry()` is exercised. Out-of-range `u` raises. After processing, peak and
DC meet S001. No sampled-audio generators.
