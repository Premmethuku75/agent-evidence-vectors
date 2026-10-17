# probityai

Python bindings for the [`jcs-admit`](https://crates.io/crates/jcs-admit) Rust crate:
admit a JSON document on its raw bytes and return its RFC 8785 canonical form, or
refuse it with the crate's own reason.

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

The extension links `jcs-admit` 0.1.2 unchanged. Every refusal is a `JcsError`
(a `ValueError`) whose `variant` and `fields` are the Rust variant and fields. The
crate's documentation is the reference for what is refused and why:
<https://docs.rs/jcs-admit/0.1.2>.

Licensed under MIT or Apache-2.0, at your option.
