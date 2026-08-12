# aee-vocabulary

A canonical, closed vocabulary for terms that describe **adversarial-execution evidence claims**:
what an executed artifact attempted, what a substrate beneath it observed or refused, how directly
and from what vantage a claim was obtained, and how much of a declared population a claim actually
covers.

This is not an identity registry, a reputation registry, or a wallet registry — see
`vocabulary.yaml`'s `out_of_scope` block. It is scoped to one question: **when a system emits a
claim about an execution, what does the claim actually say, and how would a distrusting reader
check it?**

## Why this exists

Every comparable registry in this space defines the same kind of thing — a shared vocabulary that
independent systems crosswalk their own claims onto, so a term means the same thing across
vendors. What none of them have is a name for the axis that matters most for a claim a distrusting
party has to rely on: **who observed it, and how directly.** `observation_vantage`,
`observation_directness`, `coverage_denominator`, and `does_not_assert` — the core terms here — are
the vocabulary for that axis. See `vocabulary.yaml` for full definitions and the mechanism each
term is grounded in.

## Files

- **`vocabulary.yaml`** — the registry itself. CC0-1.0 (public domain); reuse freely.
- **`GOVERNANCE.md`** — promotion/demotion rules, merge discipline, and the no-self-grounding-
  exemption rule that binds the founding maintainer's own systems identically to anyone else's.
- **`CONTRIBUTING.md`** — how to file a crosswalk.
- **`crosswalk/`** — filed crosswalks, one file per system. `TEMPLATE.yaml` is the starting point.
- **`scripts/validate_crosswalks.py`** — CI validator. Fails loudly on an unrecognized shape rather
  than silently skipping it (a defect found in a comparable registry's own validator, where 13 of
  34 filed crosswalks were invisible to the tool that was supposed to check them).

## Companion project

`vocabulary.yaml`'s `spec_anchor` points at the adversarial-execution-evidence predicate
specification, vendored and versioned in
[`astrogilda/aee-conformance`](https://github.com/astrogilda/aee-conformance) — the reference
verifier and conformance vector suite for that predicate. This registry names the vocabulary; that
repository proves an implementation actually speaks it.

## Status

`v0.1.0-draft`. The initial term set here was seeded from a first-principles audit of the nearest
comparable registry, kept honest about which terms are genuinely open ground versus genuine
overlap with existing work — see each term's `why_this_registry` note in `vocabulary.yaml` for the
specific gap it fills. Not yet tagged, not yet advertised for external filing. First external
crosswalk welcome once this reaches a tagged `v0.1.0`.
