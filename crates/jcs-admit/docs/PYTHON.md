# Python distribution

`python/` builds the `probityai` wheel: one abi3 extension that links the published
`jcs-admit` 0.1.2 and `dsse` 0.1.3 crates from crates.io, unchanged, and exposes them as
`probityai.jcs` and `probityai.dsse`. `python/twin/` builds `jcs-admit`, a pure-Python
wheel that re-exports `probityai.jcs` under the crate's name and depends on one exact
`probityai` release. Neither is on PyPI yet.

## Consumer contract

`probityai.jcs` has `admit`, `admit_ijson`, `admit_with`, `is_canonical` and
`is_canonical_with`. Each takes `bytes`; `str`, `bytearray` and `memoryview` raise
`TypeError`, because the faults the crate refuses include byte sequences no `str` can
hold. `admit_with` and `is_canonical_with` take the crate's `Options` as keyword
arguments with the crate's defaults: `max_depth=128` (saturating at 512),
`max_bytes=20971520` (`None` removes the cap), `safe_integers`, `integers_only` and
`reject_noncharacters`.

`probityai.dsse` has `pae`, `sign`, `verify` and `verify_threshold`, with
`Ed25519Signer`, `Ed25519Verifier` and `VerifiedPayload`. Envelopes cross the boundary
as their JSON bytes. `verify_threshold` counts distinct trusted keys, never signature
entries, and returns the exact bytes the signatures covered with the authenticated
payload type. `sign` takes one signer or a non-empty sequence of them.

A refusal raises `JcsError` or `DsseError`, both `ValueError`:

- `variant` is the exact Rust variant name;
- `fields` is the crate's own serialization of the variant's fields: a dict for a
  struct variant, the bare value for a one-field tuple variant, `None` for a unit
  variant, the same shapes the npm packages report;
- `str(error)` is the crate's bounded display text.

The mapping reads each crate's `serde` serialization, so a variant a crate adds later
arrives with its own name and fields.

## Build and platforms

One wheel per platform serves CPython 3.10 and later (`cp310-abi3`): manylinux 2_28 and
musllinux 1_2 on x86_64 and aarch64, macOS on x86_64 and arm64, and Windows x64, plus
an sdist. `.github/workflows/python.yml` builds them on every push and installs each
runnable wheel into a clean environment, with no source on the path, to run the whole
suite against it.

## Tests

The tests read the vector files of the exact crate releases the extension links, out
of the Cargo registry through `cargo metadata`, so the corpus under test is the one
that shipped with the code under test:

- RFC 8785 Appendix B, the reference suite, the cross-rail Go corpus, the 317
  adversarial string cases and the 850 number ties, under the profiles the crate's own
  tests use;
- the same 2,122 inputs through the crate's `wasm_oracle` example, so binding and
  native crate must agree on every output byte and every refusal's variant, fields and
  message;
- the DSSE PAE attack cases, and the go-securesystemslib cross-language vectors,
  including signatures reproduced byte for byte from the published test seed.

`python -m mypy.stubtest probityai._native` holds the type stub to the built module.

```sh
cd python
uv sync --locked
uv run --locked pytest
```
