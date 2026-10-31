# Connector scope record vectors

Thirteen cases for the `connector-scope-record/v1` record: a connector's scope
record for a health-system integration, with accepted reads and changes and
the refusals that keep a connector inside the scope it was granted.

Each refusal has an accepted twin that differs in one field, so a verifier
that passes the corpus has to decide on the scope and not on the shape.

```sh
go build -o aee-verify ./cmd/aee-verify
./aee-verify vectors-connector-scope
```

Exit 0 when every case behaves as `MANIFEST.json` declares, 1 when one does
not and is named, 2 when the corpus could not be judged.

[INDEX.md](INDEX.md) lists every case with its decision, reason code and twin.
`gen_vectors.py` writes the cases and `INDEX.md`; do not edit them by hand.
