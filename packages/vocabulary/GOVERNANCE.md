# Governance

This document binds every maintainer of this repository, including its founding maintainer. It
exists to make the registry trustworthy to a party who has no reason to trust any single
contributor — including the one who started it.

## What this registry does and does not do

This registry names terms. It does not certify implementations, does not endorse any product, and
does not adjudicate disputes about whose product is "better." A term appearing here with your
system listed as an issuer means: your system emits a value for that term, in a real running
artifact, and you have filed a crosswalk saying so. It is not an endorsement.

## No self-grounding exemption

**A maintainer's own product receives no special standing.** A crosswalk filed by a maintainer for
their own system goes through the identical review as any other filing: an independent reviewer
(not the filer) confirms the cited `source_path` actually resolves and actually carries the
declared value, before merge. This applies without exception to the founding maintainer's own
systems (the AEE predicate and its reference verifier).

## Merge discipline

- **No maintainer merges their own pull request.** Not for a typo fix, not for an urgent
  correction. A second maintainer merges, or the PR waits.
- **No direct pushes to `main`.** Every change, including maintainer changes, goes through a pull
  request with CI green.
- **Every crosswalk PR gets an independent evidence check** before merge: the reviewer fetches the
  cited `source_path` directly and confirms it resolves to the declared value. A crosswalk citing
  a `source_path` that does not resolve is not merged, regardless of who filed it.

These three rules exist because a 2026-08-11 audit of the nearest comparable registry found the
opposite of every one of them: 91 of 91 merged pull requests merged by the sole maintainer
including 25 of their own, eight self-merged in under five minutes with zero review, 87 of 193
commits on `main` as direct pushes by the maintainer, and the maintainer's own product entered
favorably into the one term section their own validator script did not check. None of that was
fraud — the maintainer's tooling was genuinely rigorous everywhere it was enforced. It was simply
unenforced in the one place it mattered most: the maintainer grading their own product. This
registry is built to not have that gap from day one, rather than retrofit it after the fact.

## Promotion and demotion

- A term starts `proposed`.
- Promotion to `canonical` requires a SECOND independently-maintained system to file a crosswalk
  declaring `evidence: emitted` with a resolvable `source_path`, verified by an independent
  reviewer per the merge discipline above. One issuer, however large, does not promote a term.
- Every `proposed` term carries a `review_by` date. If no second independent `evidence: emitted`
  issuer has surfaced by that date, the term is demoted to `reserved` and removed at the following
  review unless a production issuer surfaces in the interim.
- A demotion is recorded in the term's own history, not silently deleted — see `reserved:` in
  `vocabulary.yaml`.

## Conflict of interest

Any maintainer with a commercial or research interest in a system that has filed, or is
considering filing, a crosswalk must disclose that interest in `MAINTAINERS.md` before reviewing
any crosswalk for that system. A maintainer with a disclosed interest may not be the sole reviewer
of that system's crosswalk.

## Committer access

Committer access is granted on a sustained maintenance record — reviewing others' crosswalks
accurately over time — never on merely having filed a crosswalk or having run the validator once.

## Amending this document

Changes to this file require the same two-maintainer review as any other change, and a change
that weakens any rule in "Merge discipline" above requires a stated reason in the PR description
and a 14-day open comment window before merge, regardless of maintainer count at the time.
