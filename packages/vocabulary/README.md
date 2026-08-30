# aee-vocabulary

A canonical, closed vocabulary for terms that describe **adversarial-execution evidence claims**:
what an executed artifact attempted, what a substrate beneath it observed or refused, how directly
and from what vantage a claim was obtained, and how much of a declared population a claim actually
covers.

This is not an identity registry, a reputation registry, or a wallet registry. The out-of-scope
block in the registry file says so in the file itself. One question sets the scope: when a system
emits a claim about an execution, what does the claim actually say, and how would a distrusting
reader check it?

## Why this exists

Naming the terms in an execution-evidence claim is a well-populated space, and every registry in
it builds the same kind of thing, a shared vocabulary that independent systems crosswalk their own
claims onto so a term means one thing across vendors. What none of them have is a name for the
axis that matters most to a claim a distrusting party has to rely on: who observed it, and how
directly. Four terms here carry that axis:

- `observation_vantage` and `observation_directness` say where a claim was obtained and through
  how many hands it passed on the way.
- `coverage_denominator` and `does_not_assert` say what the claim leaves out, and say it inside
  the signed bytes.

Full definitions and their grounding mechanisms are in vocabulary.yaml.

## Files

vocabulary.yaml is the registry itself, CC0-1.0 and public domain, so reuse it freely.
GOVERNANCE.md carries the promotion and demotion rules, the merge discipline, and the
no-self-grounding-exemption rule binding the founding maintainer's own systems identically to
anyone else's. CONTRIBUTING.md says how to file a crosswalk. Filed crosswalks live one file per
system under crosswalk/, starting from TEMPLATE.yaml there.

The validator is scripts/validate_crosswalks.py, and CI runs it on every change. It fails loudly
on a file shape it does not recognize, never skipping the file quietly. A comparable registry's
validator skipped silently, and thirteen of the thirty-four crosswalks filed against it were
invisible to the tool meant to be checking them.

## Companion project

The `spec_anchor` field points at the adversarial-execution-evidence predicate specification,
vendored and versioned in
[astrogilda/aee-conformance](https://github.com/astrogilda/aee-conformance), the reference
verifier and conformance vector suite for that predicate. This registry names the vocabulary. That
repository shows an implementation speaking it.

## Status

Version 0.1.0, tagged. The initial term set came from a first-principles audit of the nearest
comparable registry, kept honest about which terms are open ground and which overlap work that
already exists. Each term carries a why_this_registry note naming the gap it fills.

Every term is meant to land as a field inside a signed statement, so a consumer is never expected
to go hunting through documentation to learn what a claim withholds. The tag exists so a crosswalk
has a fixed version to file against, not as a signal that external filings are being solicited
yet.
