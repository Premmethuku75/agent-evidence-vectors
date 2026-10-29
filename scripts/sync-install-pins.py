#!/usr/bin/env python3
"""Rewrite the pinned install lines on the inbound pages from the published release.

The published release is the one scripts/distribution-gate.py reads from
CITATION.cff (the preferred citation), not the source build version in
pyproject.toml: the source version names a build that may not be on PyPI yet,
and a README that pins it tells a stranger to install something that does not
exist. A release bumps CITATION.cff, then runs this to move every pin.

    python3 scripts/sync-install-pins.py           rewrite the pins in place
    python3 scripts/sync-install-pins.py --check   exit 1 when any pin differs
"""

from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
V = r"\d+\.\d+\.\d+"
# Per page, patterns with one group around the version. Only pins of this
# project are listed: a pin of another package, or an Action example that
# deliberately names another tag, never matches.
RULES: dict[str, tuple[str, ...]] = {
    "README.md": (
        rf"agent-evidence-vectors==({V})",
        rf"aee-verify@v({V})",
        rf"releases/tag/v({V})",
        rf"pypi\.org/project/agent-evidence-vectors/({V})/",
        rf"agent-evidence-vectors/blob/v({V})/",
        rf"At v({V}) the default corpus",
    ),
    "DISTRIBUTION.md": (
        rf"aee-verify@v({V})",
        rf"releases/tag/v({V})",
        rf"pypi\.org/project/agent-evidence-vectors/({V})/",
        rf"git checkout v({V})",
        rf"agent-evidence-vectors==({V})",
    ),
    "docs/guides/runner.md": (
        rf"agent-evidence-vectors@v({V})",
        rf"aee-verify@v({V})",
        rf"agent-evidence-vectors==({V})",
    ),
}


def published_version(root: Path) -> str:
    """The released version, by the same definition the distribution gate uses."""
    spec = importlib.util.spec_from_file_location(
        "distribution_gate", root / "scripts" / "distribution-gate.py"
    )
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load scripts/distribution-gate.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return str(module.released_version((root / "CITATION.cff").read_text()))


def _swap(match: re.Match[str], version: str) -> str:
    whole = match.group(0)
    lo, hi = match.start(1) - match.start(), match.end(1) - match.start()
    return whole[:lo] + version + whole[hi:]


def rewrite(text: str, rules: tuple[str, ...], version: str) -> str:
    for rule in rules:
        text = re.sub(rule, lambda m: _swap(m, version), text)
    return text


def sync(root: Path, version: str, apply: bool) -> list[str]:
    """Pages whose pins differ from `version`; with apply, rewrite them."""
    stale = []
    for rel, rules in RULES.items():
        path = root / rel
        old = path.read_text()
        new = rewrite(old, rules, version)
        if new != old:
            stale.append(rel)
            if apply:
                path.write_text(new)
    return stale


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="fail instead of rewriting")
    args = parser.parse_args()
    version = published_version(ROOT)
    stale = sync(ROOT, version, apply=not args.check)
    if args.check and stale:
        print(f"install pins differ from published release {version}: {', '.join(stale)}")
        print("fix: python3 scripts/sync-install-pins.py")
        return 1
    if args.check:
        print(f"install pins match published release {version}")
    else:
        print(f"pins set to {version}: {stale or 'unchanged'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
