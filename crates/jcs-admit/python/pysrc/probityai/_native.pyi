# Type stub for the compiled extension. CI runs `python -m mypy.stubtest
# probityai._native` against the built module, so a binding change that is not
# reflected here fails the build.

from typing import Any, Final

__all__ = [
    "DEFAULT_MAX_BYTES",
    "DEFAULT_MAX_DEPTH",
    "JCS_ADMIT_VERSION",
    "JcsError",
    "MAX_SUPPORTED_DEPTH",
    "admit",
    "admit_ijson",
    "admit_with",
    "is_canonical",
    "is_canonical_with",
]

DEFAULT_MAX_DEPTH: Final[int]
MAX_SUPPORTED_DEPTH: Final[int]
DEFAULT_MAX_BYTES: Final[int]
JCS_ADMIT_VERSION: Final[str]

class JcsError(ValueError):
    variant: str
    fields: Any

def admit(data: bytes, /) -> bytes: ...
def admit_ijson(data: bytes, /) -> bytes: ...
def admit_with(
    data: bytes,
    /,
    *,
    max_depth: int = 128,
    max_bytes: int | None = 20971520,
    safe_integers: bool = False,
    integers_only: bool = False,
    reject_noncharacters: bool = False,
) -> bytes: ...
def is_canonical(data: bytes, /) -> bool: ...
def is_canonical_with(
    data: bytes,
    /,
    *,
    max_depth: int = 128,
    max_bytes: int | None = 20971520,
    safe_integers: bool = False,
    integers_only: bool = False,
    reject_noncharacters: bool = False,
) -> bool: ...
