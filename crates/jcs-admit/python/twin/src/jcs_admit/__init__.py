"""The jcs-admit Rust crate as a Python module.

The same objects as :mod:`probityai.jcs`, re-exported under the crate's name.
"""

from importlib.metadata import version as _version

from probityai.jcs import (
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

__version__ = _version("jcs-admit")
