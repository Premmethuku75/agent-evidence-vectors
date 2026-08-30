# Governance

This document binds every maintainer of this repository, including its founding maintainer. It
exists to make the registry trustworthy to a party who has no reason to trust any single
contributor, the one who started it included.

## What this registry does and does not do

This registry names terms. It does not certify implementations, does not endorse any product, and
does not adjudicate disputes about whose product is "better." A term appearing here with your
system listed as an issuer means one thing: your system emits a value for that term, in a real
running artifact, and you have filed a crosswalk saying so. It is not an endorsement.

## No self-grounding exemption

**A maintainer's own product receives no special standing.** A crosswalk filed by a maintainer for
their own system goes through the identical review any other filing gets. An independent reviewer,
never the maintainer who filed it, confirms before merge that the cited `source_path` resolves and
carries the declared value. This binds the founding maintainer's own systems without exception,
meaning the AEE predicate and its reference verifier.

## Merge discipline

- No maintainer merges their own pull request. Not for a typo fix, not for an urgent correction. A
  second maintainer merges, or the pull request waits.
- No direct pushes to `main`. Every change, maintainer changes included, goes through a pull
  request with CI green.
- Every crosswalk pull request gets an independent evidence check before merge. The reviewer
  fetches the cited `source_path` directly and confirms it resolves to the declared value. A
  crosswalk citing a path that does not resolve is not merged, regardless of who filed it.

Those three rules all guard one failure, and it is not fraud. A registry usually starts as one
person's careful work, and that person is normally the most rigorous participant in it. The gap
opens where the rigor is not mechanically enforced, and the place that reliably escapes enforcement
is the maintainer's own entry, because reviewing it is the one review nobody is available for.

So the rules are written to bind here first. A maintainer's crosswalk is reviewed by someone with no
declared interest in the system it describes, and if this project has no such reviewer for a given
filing, that filing waits. Promotion needs an emitter that is not us. Every cited source path is
fetched and confirmed by hand before a merge, including ours.

The measurable consequence at version 0.1.0 is that no term here is canonical, because our own
issuer does not count toward a promotion and nobody else has filed yet. That is the rule working
against the person who wrote it, which is the only evidence that it is a rule at all.

## Promotion and demotion

A term starts as proposed. Promotion to canonical requires a SECOND independently-maintained
system to file a crosswalk declaring `evidence: emitted` with a resolvable path, verified by an
independent reviewer per the merge discipline above. One issuer, however large, does not promote a
term.

Every proposed term carries a review-by date. If no second independent issuer emitting the term
has surfaced by that date, the term is demoted to reserved, and removed at the following review
unless a production issuer surfaces before then. A demotion is recorded in the term's own
history, in the reserved block at the foot of `vocabulary.yaml`, not silently deleted.

## Conflict of interest

Any maintainer with a commercial or research interest in a system that has filed, or is
considering filing, a crosswalk must disclose that interest in MAINTAINERS.md before reviewing any
crosswalk for that system. A maintainer with a disclosed interest may not be the sole reviewer of
that system's crosswalk.

## Committer access

Committer access is granted on a sustained maintenance record, meaning reviewing other people's
crosswalks accurately over time. Filing a crosswalk earns none, and running the validator once
earns none.

## Amending this document

Changes to this file require the same two-maintainer review as any other change. A change that
weakens any rule under "Merge discipline" above additionally requires a stated reason in the pull
request description and a 14-day open comment window before merge, regardless of how many
maintainers there are at the time.
