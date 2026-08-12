# Contributing a crosswalk

A crosswalk maps YOUR system's own emitted claims onto the terms in `vocabulary.yaml`. Filing one
does not require our permission to build your system, does not require us to agree your system is
good, and does not transfer any ownership of your terminology to us. It is a public, checkable
statement: "here is where my system's claims and this registry's terms agree, and here is where
they honestly don't."

## Before you file

1. Read `vocabulary.yaml` in full. Note which terms are `canonical` (an established, promoted
   definition) versus `proposed` (has a `review_by` date and needs a second independent issuer to
   promote).
2. Read `GOVERNANCE.md`. In particular: your crosswalk will be reviewed by a maintainer who does
   NOT have a declared interest in your system, and a maintainer's own systems get no exemption
   from this review.
3. Decide your match type per term, honestly, using `crosswalk_match_types` in `vocabulary.yaml`.
   `no_mapping` is a legitimate, valuable answer. A stretched `partial` claim that doesn't survive
   a reviewer fetching your `source_path` will be rejected, not quietly downgraded.

## Required shape

Copy `crosswalk/TEMPLATE.yaml` to `crosswalk/<your-system-name>.yaml`. The validated shape is the
ONLY shape: a top-level `system:` block, then one entry per registry section
(`evidence_dimensions:`, `posture_and_coverage:`, `outcome_lattice:`, `system_attributes:`) keyed
by the exact term names in `vocabulary.yaml`, each with a `match:` field using one of the five
values in `crosswalk_match_types`. **A crosswalk in any other shape (a flat `mapping:` list, a
top-level array, anything the validator does not recognize) will not render in the published
matrix and will not be merged.** This is a hard requirement, not a style preference: a
comparable registry's own crosswalk corpus was found to have thirteen of thirty-four filed
crosswalks silently invisible to its own validator because they used an unrecognized shape.

For every term you claim `exact`, `structural`, or `partial` on:

- **`evidence:`** — one of `emitted`, `inferred`, or `asserted`, per `crosswalk_evidence_states` in
  `vocabulary.yaml`. Claiming `emitted` when the reviewer cannot independently fetch and confirm
  the value is the single fastest way to get a crosswalk rejected.
- **`source_path:`** — where in your own real, running artifact this value actually lives. A file
  path, a JSON pointer into a real example output, or a URL to a real endpoint. Not a plan, not a
  roadmap item, not a field that exists in your schema but has no producer.
- **`divergences:`** (for `partial` only) — the specific, material way your claim differs from the
  canonical definition. Vague language here ("similar but not identical") will be sent back for a
  concrete list.

For every `no_mapping` term, a one-line `notes:` explaining why is enough. You do not owe us a
long justification for ground you don't claim.

## Review

- A reviewer without a declared interest in your system checks that every cited `source_path`
  resolves and actually carries the declared value.
- `scripts/validate_crosswalks.py` runs in CI on every PR and checks shape, enum membership, and
  `source_path` resolvability where the path is a public URL. It does not replace the human
  fetch-and-confirm step for anything non-public.
- Expect real scrutiny, applied identically regardless of who you are. See `GOVERNANCE.md`'s "No
  self-grounding exemption" — the founding maintainer's own systems get the same treatment.

## Proposing a new term

If your system emits something this registry has no name for, open an issue first stating the gap,
what your system does, and why the existing terms don't cover it — before opening a PR. This lets
a maintainer confirm it's a genuine gap (not a `non_equivalent_similar_label` case in disguise)
before you do the work of drafting the term.

## Filing on behalf of another system

You may file a crosswalk for a system you do not maintain, mapping it from its own public
documentation — mark `third_party_authored: true` in the crosswalk header and cite what you read.
This is explicitly welcome: it is how the registry can cover systems whose own maintainers haven't
gotten to filing yet. A third-party-authored crosswalk carries a standing invitation for the
described system's actual maintainer to correct or reclaim it, noted visibly in the file.
