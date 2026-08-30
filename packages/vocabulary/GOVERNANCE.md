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

- No maintainer merges their own pull request. Not for a typo fix, not for an urgent correction. A
  second maintainer merges, or the pull request waits.
- No direct pushes to `main`. Every change, maintainer changes included, goes through a pull
  request with CI green.
- Every crosswalk pull request gets an independent evidence check before merge. The reviewer
  fetches the cited `source_path` directly and confirms it resolves to the declared value. A
  crosswalk citing a path that does not resolve is not merged, regardless of who filed it.

### What those rules mean with one maintainer, stated because it is not obvious

Read together they mean nothing merges. Every change needs a pull request, no maintainer merges
their own, and there is one maintainer. That is not a loophole discovered later; it is the
arithmetic, and until a second maintainer holds the role it applies to routine repository work as
much as to anything else.

What actually happened, measured on 2026-08-30 and not recalled: no pull request has ever been
opened here, the history carries no merge commit, and every commit including the ones repairing
this file arrived by direct push. So the second rule above has been broken on every commit since the
repository began.

Two of the three rules are suspended until a second maintainer is added, and they suspend
themselves: the moment `MAINTAINERS.md` carries a second row, no-self-merge and
pull-requests-for-everything bind normally with nothing to re-enable. Until then repository
maintenance is direct-pushed and this paragraph is the disclosure.

**The third rule is not suspended and does not depend on maintainer count.** No crosswalk merges
without an independent evidence check by someone with no declared interest in the system it
describes. No such reviewer exists here yet, so none has merged. This registry's credibility rests on
that rule, and suspending it for convenience would retire the reason the repository exists.

Those three rules all guard one failure, and it is not fraud. A registry usually starts as one
person's careful work, and that person is normally the most rigorous participant in it. The gap
opens where the rigor is not mechanically enforced, and the place that reliably escapes enforcement
is the maintainer's own entry, because reviewing it is the one review nobody is available for.

So the rules are written to bind here first. A maintainer's crosswalk is reviewed by someone with no
declared interest in the system it describes, and if this project has no such reviewer for a given
filing, that filing waits. Promotion needs an emitter that is not us. Every cited source path is
fetched and confirmed by hand before a merge, including ours.

The measurable consequence at 0.1.1 is that no term here is canonical, because our own issuer does
not count toward a promotion and nobody else has filed. Version 0.1.0 was different: six terms
carried canonical status on our own issuer alone. The v0.1.0 tag is still reachable, so both halves
of this paragraph can be checked against the repository.

Demoting those six is the evidence here, and the current state is not. A rule that has never had to
move against the person who wrote it has not yet been tested.

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

Any maintainer with a commercial or research interest in a system that has filed, or is considering
filing, must disclose that interest in MAINTAINERS.md before reviewing anything from that system,
and may never be its sole reviewer.

## Committer access

Committer access is granted on a sustained maintenance record, meaning reviewing other people's
crosswalks accurately over time. Filing one earns none, and running the validator once earns none.

## Amending this document

Changes to this file take the same route as any other change, so today that means a direct push
under the suspension above, and it means a second-maintainer merge from the moment a second row
exists in MAINTAINERS.md.

One requirement does not move with the suspension. A change weakening any rule under Merge
discipline needs a stated reason and a 14-day open comment window before it lands, whatever the
maintainer count is at the time.

The suspension above is such a weakening and it did not get its window. It was written and amended
inside twenty minutes on 2026-08-30, on a private repository carrying no open pull request and no
open issue, so no venue for a comment window existed and nobody was there to comment. Of the two
requirements the paragraph above satisfies one: it states its reason. It does not satisfy the
window. Describing a half-met requirement as met is the same defect this section was written to
disclose, one level up.

So the suspension is provisional. Its window runs for 14 days from the day this repository becomes
readable, in whatever venue readers then have, and it stands or is withdrawn on what that produces.
This paragraph is the disclosure that it has not yet been earned.
