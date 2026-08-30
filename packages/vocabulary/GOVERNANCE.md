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
meaning the adversarial-execution-evidence predicate, abbreviated AEE, and its reference
verifier.

## Merge discipline

One rule is absolute and never depends on how many maintainers exist:

- **Every crosswalk gets an independent evidence check before merge.** The reviewer fetches the
  cited `source_path` and confirms it resolves to the declared value. A crosswalk citing a path
  that does not resolve is not merged, regardless of who filed it, and a maintainer never reviews
  a filing for a system they have a declared interest in. This is what the registry's claims rest
  on, and no count of maintainers loosens it.

Two more bind from the moment a second row exists in MAINTAINERS.md, and they arm themselves with
nothing to switch on:

- No maintainer merges their own pull request.
- No direct pushes to `main`. Every change goes through a pull request with CI green.

**With one maintainer those two would mean nothing merges at all, so they do not apply yet, and
this document says so where a reader will find it.** Every commit here has been a direct push, no
pull request has ever been opened, and the history carries zero merge commits. That is the honest
state of a registry built by one person, and it costs the reader nothing: the rule their trust
actually depends on is the first one, and that one has never been relaxed.

The single rule guards a single failure, and it is not fraud. A registry usually starts as one
person's careful work, and that person is normally its most rigorous participant. The gap opens
where rigor is not mechanically enforced, and the place that reliably escapes enforcement is the
maintainer's own entry, because reviewing it is the one review nobody is available for.

So it binds here first. No reviewer without a declared interest exists yet, so no crosswalk has
merged, including ours. Promotion needs an emitter that is not us. Every cited path is fetched by
hand before a merge, ours included.

The measurable consequence at 0.1.1 is that not one term here is canonical, because our own issuer
does not count toward a promotion and nobody else has filed. Version 0.1.0 was different: six terms
carried canonical status on our own issuer alone. That tag is still reachable, so both halves of
this paragraph can be checked against the repository.

Demoting those six is the evidence, and the current state is not. A rule that has never had to move
against the person who wrote it has not yet been tested.

## Promotion and demotion

A term starts as proposed. Promotion to canonical requires a SECOND independently-maintained
system to file a crosswalk declaring `evidence: emitted` with a resolvable path, verified by an
independent reviewer per the merge discipline above. One issuer, however large, does not promote a
term.

Every proposed term carries a review-by date. If no second independent issuer emitting the term
has surfaced by that date, the term is demoted to reserved, and removed at the following review
unless a production issuer surfaces before then. A demoted term moves into the reserved block at
the foot of `vocabulary.yaml` and is not silently deleted. That block holds two kinds of row and
each says which it is: a term explicitly declined before it was ever proposed, and a term that was
proposed and found none.

## Conflict of interest

Any maintainer with a commercial or research interest in a system that has filed, or is considering
filing, must disclose that interest in MAINTAINERS.md before reviewing anything from that system,
and may never be its sole reviewer.

## Committer access

Committer access is granted on a sustained maintenance record, meaning reviewing other people's
crosswalks accurately over time. Filing one earns none, and running the validator once earns none.

Nobody holds that record yet, the founding maintainer included, because no crosswalk has ever been
filed and so none has ever been reviewed. The first person to earn committer access here will earn
it that way. Stated plainly so a reader testing the rule against the repository finds the answer
already written down.

## Amending this document

A change that weakens the crosswalk evidence check needs a stated reason and a 14-day open comment
window before it lands, whatever the maintainer count is. That rule is the registry's whole claim,
so it is the one change nobody makes quietly, and the window applies to the person who wrote it as
much as to anyone else.

Everything else in this file follows the merge discipline above: direct while there is one
maintainer, second-maintainer merge from the moment there are two.
