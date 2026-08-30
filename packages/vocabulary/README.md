# aee-vocabulary

A canonical, closed vocabulary for terms that describe **adversarial-execution evidence claims**:
what an executed artifact attempted, what a substrate beneath it observed or refused, how directly
and from what vantage a claim was obtained, and how much of a declared population a claim actually
covers.

One question sets the scope. When a system emits a claim about an execution, what does that claim
actually say, and how would a reader who trusts nobody check it? Identity, reputation and wallets
belong to other registries, and the out-of-scope block says so in the registry file itself, where a
parser can reach it.

## Why this exists

Naming the terms in an execution-evidence claim is a well-populated space. The registries in it
share a purpose: a vocabulary that independent systems crosswalk their own claims onto, so that a
term means one thing across vendors.

Four terms here carry the axis that decides whether any of the rest can be relied on, which is who
observed the execution and through how many hands the account of it passed:

- `observation_vantage` and `observation_directness` say where a claim was obtained and how
  directly.
- `coverage_denominator` and `does_not_assert` say what the claim leaves out, and say it inside the
  signed bytes.

Full definitions and their grounding mechanisms are in vocabulary.yaml.

## Files

vocabulary.yaml is the registry itself, CC0-1.0 and public domain, so reuse it freely.
GOVERNANCE.md carries the promotion and demotion rules, the merge discipline, and the
no-self-grounding-exemption rule binding the founding maintainer's own systems identically to
anyone else's. CONTRIBUTING.md says how to file a crosswalk. Filed crosswalks live one file per
system under crosswalk/, starting from TEMPLATE.yaml there.

The validator is scripts/validate_crosswalks.py, and CI runs it on every change. Hand it a file
whose shape it does not recognize and it fails, loudly, naming the file.

The usual alternative is silence. A validator that skips what it cannot parse still reports a clean
run, over crosswalks it never opened, and the filer who got the shape wrong is told nothing at all.
The unrecognized-shape branch is a dozen lines. Read it and check.

## Companion project

The `spec_anchor` field points at the adversarial-execution-evidence predicate specification,
vendored and versioned in
[astrogilda/aee-conformance](https://github.com/astrogilda/aee-conformance), the reference verifier
and conformance vector suite for that predicate, which is where the vocabulary defined here is
actually spoken.

## Status

Version 0.1.1.

The initial term set came from reading the nearest comparable registry term by term and recording,
for each of ours, whether it names ground nobody has named yet or overlaps something already in
use. Both answers occur. Five of the eight terms carry a why_this_registry note saying which, and
that note is a field in the file, so a reader who disagrees can point at the line. The other three
make their case in the definition itself.

Every term is meant to land as a field inside a signed statement. Nobody consuming one should have
to go hunting through documentation to learn what a claim withholds. The tag gives a crosswalk a
fixed version to file against; external filings are not being solicited yet.
