"""Probity AI: canonical JSON admission and DSSE signing for evidence records.

``probityai.jcs`` admits a JSON document and returns its RFC 8785 canonical
bytes, refusing duplicate members, unsafe strings and unbounded nesting on the
raw bytes first. Both come from Rust crates published on crates.io and linked
into this wheel unchanged.
"""

from importlib.metadata import version as _version

from probityai import jcs

__all__ = ["jcs"]

__version__ = _version("probityai")
