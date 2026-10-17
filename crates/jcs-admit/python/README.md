# probityai

Python bindings for two Rust crates: [`jcs-admit`](https://crates.io/crates/jcs-admit)
admits a JSON document on its raw bytes and returns its RFC 8785 canonical form, and
[`dsse`](https://crates.io/crates/dsse) signs and verifies DSSE envelopes, counting a
threshold over distinct keys.

```sh
pip install probityai==0.1.0
```

```python
from probityai import jcs

jcs.admit(b'{ "b": 1, "a": [1.0, 1e30] }')  # b'{"a":[1,1e+30],"b":1}'

try:
    jcs.admit(b'{"a":1,"a":2}')
except jcs.JcsError as e:
    print(e.variant, e.fields)  # DuplicateMember {'name': 'a', 'offset': 7}
```

```python
import os
from probityai import dsse

harness = dsse.Ed25519Signer(os.urandom(32), key_id="harness")
witness = dsse.Ed25519Signer(os.urandom(32), key_id="witness")
envelope = dsse.sign("application/vnd.in-toto+json", b'{"a":1}', [harness, witness])
verified = dsse.verify_threshold(envelope, [harness.verifier(), witness.verifier()], 2)
print(verified.payload_type, verified.payload, verified.accepted_keys)
```

The extension links `jcs-admit` 0.1.2 and `dsse` 0.1.3 unchanged. Every refusal is
a `JcsError` or a `DsseError` (both `ValueError`) whose `variant` and `fields` are
the Rust variant and fields. Each crate's documentation is the reference for what
it refuses and why: <https://docs.rs/jcs-admit/0.1.2> and <https://docs.rs/dsse/0.1.3>.

Licensed under MIT or Apache-2.0, at your option.
