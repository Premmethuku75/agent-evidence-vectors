# jcs-admit

Admit a JSON document on its raw bytes and return its RFC 8785 canonical form,
refusing duplicate members, unsafe strings and unbounded nesting first. This is the
[`jcs-admit`](https://crates.io/crates/jcs-admit) Rust crate, version 0.1.2, as a
Python module.

```sh
pip install jcs-admit==0.1.2
```

```python
import jcs_admit

jcs_admit.admit(b'{ "b": 1, "a": [1.0, 1e30] }')  # b'{"a":[1,1e+30],"b":1}'
```

The module is `probityai.jcs` under the crate's name: it installs `probityai`
0.1.0, which links the crate, and re-exports the same functions and the same
`JcsError`. Use `probityai` directly for DSSE signing as well.

Licensed under MIT or Apache-2.0, at your option.
