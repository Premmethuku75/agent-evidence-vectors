# Contributing a crosswalk

A crosswalk maps YOUR system's own emitted claims onto the terms in vocabulary.yaml. Filing one
does not require our permission to build your system, does not require us to agree your system is
good, and does not transfer any ownership of your terminology to us. It is a public, checkable
statement: "here is where my system's claims and this registry's terms agree, and here is where
they honestly don't."

## Before you file

Read the registry file in full, and read every status key while you are in there. At version 0.1.1
each one says proposed, which means the term carries a review_by date and still needs a second
independent issuer before promotion. Nothing here is canonical yet, and the reason is that nobody
has filed a crosswalk at all, us included. Your filing is what moves a term, and the maintainer's
own systems are held to the same bar, which is why they have not moved one either.

Read GOVERNANCE.md as well. In particular, your crosswalk will be reviewed by a maintainer who
does NOT have a declared interest in your system, and a maintainer's own systems get no exemption
from that review.

Then decide your match type per term, honestly, using the crosswalk_match_types block in the
registry. Answering no_mapping is a legitimate and valuable answer. A stretched partial claim that
does not survive a reviewer fetching the source path you cited will be rejected.

## Required shape

Copy `crosswalk/TEMPLATE.yaml` to `crosswalk/<your-system-name>.yaml`. The validated shape is the
only shape: four required top-level keys, an optional maintainer block, then one entry per registry
section, keyed by the exact term names the registry uses, each carrying a match field set to one of
the values in crosswalk_match_types. A claim of exact, structural or partial needs two more fields
per term, `evidence` and `source_path`, and a partial claim needs a third, `divergences`. All three
are described below. A file built from this paragraph alone is refused, and the refusal names
whichever of them is missing.

Check it before you open anything: `python3 scripts/validate_crosswalks.py` runs the same code CI
runs, needs only pyyaml, and names the file and the rule when it refuses.

The four the validator will refuse a file for missing are `system`, `system_url`,
`crosswalk_version` and `vocabulary_version_targeted`. `system` is a plain string, not a block.

The example below is a complete, valid file. It is checked against the validator by
`scripts/test_contributing_example.py`, so a change to either the required keys or this block that
leaves the two disagreeing turns CI red. An earlier version of this section showed a shape the
validator rejects for three missing keys, and nothing noticed, because nobody had run the
instructions.

```yaml
system: your-system-name
system_url: https://example.invalid/your/system
crosswalk_version: "0.1.0"
vocabulary_version_targeted: "0.1.1"

maintainer:
  github: your-github-handle
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
      - reconstructed values come from a nightly diff, never from a live capture

posture_and_coverage:
  coverage_denominator:
    match: no_mapping
    notes: this system publishes no committed population for its findings
```

**A crosswalk in any other shape, a flat mapping list, a top-level array, anything the validator
does not recognize, will not be merged.** The validator
refuses such a file by name and CI goes red, so you find out on your first push. The alternative is
a validator that skips a shape it was never taught: the run stays green, your file sits in the
directory mapping nothing, and you learn nothing until somebody notices the gap months later.

On every term you claim exact, structural, or partial on, three fields do the work. The
evidence field takes one of emitted, inferred, or asserted, per crosswalk_evidence_states in the
registry; claiming emitted when the reviewer cannot independently fetch and confirm the value is
the fastest way to get a crosswalk rejected. The source path says where in your own running
artifact the value lives, as a file path, a JSON pointer into a real example output, or a URL to a
real endpoint. A path resolves against something that runs, where a plan, a roadmap item, or a
schema field with no producer behind it resolves against nothing.

Two things check that path and only one of them can stop you. The validator reaches it on an emitted
claim, and what it reports is a warning, so no source path turns CI red by itself. The check that
decides is the human one in GOVERNANCE: a reviewer fetches the path, confirms it resolves to the
declared value, and does not merge a crosswalk whose path does not resolve. The divergences field, which a
partial claim needs and no other claim uses, names the material way your claim differs from the
registry's own definition; vague language there, "similar but not identical" and the like, gets sent
back for a concrete list.

For every no_mapping term, a one-line note explaining why is enough. You do not owe us a long
justification for ground you don't claim.

## Review

- A reviewer without a declared interest in your system checks that every cited source path
  resolves and actually carries the declared value.
- The validator under scripts/ runs in CI on every pull request and checks shape, enum membership,
  and, on an emitted claim whose path is a public URL, whether that URL answers a HEAD request. It
  reports that last one as a warning and never a failure, so it cannot refuse a merge on its own and
  does not replace the human
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
yet. The `third_party_authored: true` marker is what a described system's own maintainer looks for:
it says the mapping was made from outside, so correcting or reclaiming it needs no argument about
who filed first.
