# Proposed OpenCRE links

[`opencre-links.json`](../opencre-links.json) gives OpenCRE three concrete links
to review: recomputing a result, checking observation vantage, and naming coverage
gaps. Each row pairs a vocabulary term with an accepting and a rejecting
observed-effect example. The rows target CRE `307-507`; OpenCRE has not accepted
this proposal.

The vocabulary source is v0.3.0 at
`78225a7b2b6d30518f77f7d7a88df2f648008d5d`. The vector examples come from v0.16.0
at `8d6295fb5db3e57c52df09f2fbeeb758b09f5c7d`. Their observed-effect corpus digest
is `d708b2d69d7051adbc2f5c849a43f03e4330b0e36a05ac099948b5af33dbd042`.

These are proposed control links, not an issuer crosswalk or a term promotion.
The `match` and `basis` fields describe the actual fit. Agreement recomputation
is one example of derived-result checking; it does not implement the whole AEE
result lattice. Vantage labels need a consumer's trust policy. Path gaps and
committed population denominators express different coverage models, so that
row is a partial mapping. A passing fixture supplies no outside observer.

The row shape retains `id`, `name`, `permalink`, `vector`, and `opencre[].id`,
with accepting controls and review status added. This follows the separate-import
request in [OpenCRE #1045](https://github.com/OWASP/OpenCRE/issues/1045).
Corrections should name the row, the source requirement, and the case that changes
its interpretation.
