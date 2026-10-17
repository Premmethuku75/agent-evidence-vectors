"""Probity AI: canonical JSON admission and DSSE signing for evidence records.

``probityai.jcs`` admits a JSON document and returns its RFC 8785 canonical
bytes, refusing duplicate members, unsafe strings and unbounded nesting on the
raw bytes first. ``probityai.dsse`` signs and verifies DSSE envelopes over the
pre-authentication encoding, with threshold verification over distinct keys.
Both come from Rust crates published on crates.io and linked into this wheel
unchanged.
"""

from importlib.metadata import version as _version

from probityai import dsse, jcs

__all__ = ["dsse", "jcs"]

__version__ = _version("probityai")
