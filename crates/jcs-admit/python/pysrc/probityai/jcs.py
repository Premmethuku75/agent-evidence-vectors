"""Admission and RFC 8785 canonicalization, bound from the ``jcs-admit`` crate.

Every function takes ``bytes``. A ``str`` raises ``TypeError``: the refusals
this module exists for include byte sequences that no ``str`` can hold.

A refusal raises :class:`JcsError`. ``error.variant`` is the Rust variant name
(``"DuplicateMember"``, ``"TooDeep"`` and so on) and ``error.fields`` its fields
with their Rust names, the same pair the crate serializes and the npm package
reports.

>>> from probityai import jcs
>>> jcs.admit(b'{ "b": 1, "a": [1.0, 1e30] }')
b'{"a":[1,1e+30],"b":1}'
"""

from probityai._native import (
    DEFAULT_MAX_BYTES,
    DEFAULT_MAX_DEPTH,
    JCS_ADMIT_VERSION,
    MAX_SUPPORTED_DEPTH,
    JcsError,
    admit,
    admit_ijson,
    admit_with,
    is_canonical,
    is_canonical_with,
)

__all__ = [
    "DEFAULT_MAX_BYTES",
    "DEFAULT_MAX_DEPTH",
    "JCS_ADMIT_VERSION",
    "MAX_SUPPORTED_DEPTH",
    "JcsError",
    "admit",
    "admit_ijson",
    "admit_with",
    "is_canonical",
    "is_canonical_with",
]
