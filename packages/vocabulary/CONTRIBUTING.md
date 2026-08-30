# Contributing a crosswalk

A crosswalk maps YOUR system's own emitted claims onto the terms in `vocabulary.yaml`. Filing one
does not require our permission to build your system, does not require us to agree your system is
good, and does not transfer any ownership of your terminology to us. It is a public, checkable
statement: "here is where my system's claims and this registry's terms agree, and here is where
they honestly don't."

## Before you file

Read the registry file in full. Note which terms are canonical, meaning an established and
promoted definition, and which are proposed, meaning the term carries a review_by date and needs a
second independent issuer before it can be promoted.

Read GOVERNANCE.md as well. In particular, your crosswalk will be reviewed by a maintainer who
does NOT have a declared interest in your system, and a maintainer's own systems get no exemption
from that review.

Then decide your match type per term, honestly, using the crosswalk_match_types block in the
registry. Answering no_mapping is a legitimate and valuable answer. A stretched partial claim that
does not survive a reviewer fetching the source path you cited will be rejected.

## Required shape

Copy the crosswalk template to `crosswalk/<your-system-name>.yaml`. The validated shape is the
only shape: a top-level system block, then one entry per registry section, keyed by the exact term
names the registry uses, each carrying a match field set to one of the five values in
crosswalk_match_types.

```yaml
system:
  name: your-system-name
  repository: https://example.invalid/your/system
  third_party_authored: false

evidence_dimensions:
  observation_vantage:
    match: exact
    evidence: emitted
    source_path: schema/claim.json#/properties/basis
  observation_directness:
    match: partial
    evidence: emitted
    source_path: https://example.invalid/claims/latest.json
    divergences:
      - reconstructed values come from a nightly diff, not from a live capture

posture_and_coverage:
  coverage_denominator:
    match: no_mapping
    notes: this system publishes no committed population for its findings
```

**A crosswalk in any other shape, a flat mapping list, a top-level array, anything the validator
does not recognize, will not render in the published matrix and will not be merged.** A
comparable registry's own corpus turned out to have thirteen of its thirty-four filed crosswalks
invisible to its own validator, each of them in a shape the validator had never been taught.

On every term you claim exact, structural, or partial on, three fields do the work. The
evidence field takes one of emitted, inferred, or asserted, per crosswalk_evidence_states in the
registry; claiming emitted when the reviewer cannot independently fetch and confirm the value is
the fastest way to get a crosswalk rejected. The source path says where in your own running
artifact the value lives, as a file path, a JSON pointer into a real example output, or a URL to a
real endpoint. A path resolves against something that runs, where a plan, a roadmap item, or a
schema field with no producer behind it resolves against nothing. The divergences field, which a
partial claim needs and no other claim uses, names the material way your claim differs from the
canonical definition; vague language there, "similar but not identical" and the like, gets sent
back for a concrete list.

For every no_mapping term, a one-line note explaining why is enough. You do not owe us a long
justification for ground you don't claim.

## Review

- A reviewer without a declared interest in your system checks that every cited source path
  resolves and actually carries the declared value.
- The validator under scripts/ runs in CI on every pull request and checks shape, enum membership,
  and source-path resolvability wherever the path is a public URL. It does not replace the human
  fetch-and-confirm step for anything non-public.

Expect real scrutiny, applied identically regardless of who you are. The "No self-grounding
exemption" section of GOVERNANCE.md writes that down: the founding maintainer's own systems get
exactly the treatment yours does. Scrutiny here is visible, too. A claim that fails the evidence
check comes back to you with the reason attached, and never gets quietly downgraded to a weaker
match on its way through.

## Proposing a new term

If your system emits something this registry has no name for, open an issue before you open a pull
request, stating the gap, what your system does, and why the existing terms don't cover it. That
lets a maintainer confirm it is a genuine gap, not a non_equivalent_similar_label case in
disguise, before you do the work of drafting the term.

## Filing on behalf of another system

You may file a crosswalk for a system you do not maintain, mapping it from its own public
documentation. Mark `third_party_authored: true` in the crosswalk header and cite what you read.
This is welcome: it is how the registry covers systems whose own maintainers haven't got to filing
yet. Such a crosswalk carries a standing invitation, visible in the file, for the described
system's actual maintainer to correct or reclaim it.
