#!/usr/bin/env python3
"""Tests for the identity rules in pre-push-identity-scan.py and its siblings.

WHY THIS FILE EXISTS. This repository is public. What it must never carry is a
path from it to the website: the website host in any spelling. Other private
product names, absolute home paths and private dossier names are refused too.
What it may carry is its own organisation's name, the verifier's name and the
bare word both are built on, in any form -- a clone URL, a schema string, an
environment variable, a sentence. A name by itself connects nothing to
anything, so a guard that refuses it is refusing the wrong thing.

A loosening that goes unnoticed is indistinguishable from the control working,
and so is a tightening that refuses legitimate work. So every case below asserts
a direction, against every guard this repository carries: the history scanner,
the content scanner and the commit-message gate.

The tokens are built from hex at run time, exactly as the scanner holds its own,
so this file can be read by anyone without carrying the strings it is about.

Usage: python3 scripts/pre-push-identity-scan-test.py
Exit 0 when every case holds; 1 on a summary of the failures.
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
from collections.abc import Callable, Sequence
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("scan", HERE / "pre-push-identity-scan.py")
assert _spec is not None and _spec.loader is not None
scan = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(scan)


def _hex(value: str) -> str:
    return bytes.fromhex(value).decode("ascii")


OWNER = _hex("70726f626974796169")
COMPANY = _hex("70726f62697479")
SITE = _hex("67657470726f62697479") + ".dev"
OTHER = _hex("6d617463686c6f636b")
ORG_NAME = COMPANY.title() + " AI"
VERIFIER_REPO = COMPANY + "-verify"
VERIFIER_ENV = COMPANY.upper() + "_VERIFY_COMMAND"
POLICY_SCHEMA = COMPANY + "-policy/v1"
CASE_SCHEMA = COMPANY + "-case/v1"
ESCAPED_JSON_HOST = "\\u0067" + SITE[1:]
ESCAPED_HTML_HOST = "&#103;" + SITE[1:]
# Joined from parts so that no line of this file is itself a hit: the history
# scanner reads every line this file adds.
HOME_PATH = "/".join(("", "home", "someone", "notes.txt"))
DOSSIER_PATH = "/".join(("research", "123-private-dossier"))
THIRD_PRODUCT = "-".join(("mcp", "test", "toolkit"))

_sidecar = scan.Sidecar()


def refused(line: str) -> bool:
    """Whether the scanner would report this as an added line."""
    scanned = scan.permit("+" + line)
    if any(rule.search(scanned) for _, rule in scan.RULES):
        return True
    return bool(_sidecar.labels(scanned[1:]))


PERMITTED = (
    ("an owner-qualified path", f"{OWNER}/agent-evidence-vectors"),
    ("a web URL", f"https://github.com/{OWNER}/agent-evidence-vocabulary/blob/main/README.md"),
    ("an ssh URL", f"git@github.com:{OWNER}/agent-evidence-admission.git"),
    ("a package source URL", f"git+https://github.com/{OWNER}/agent-evidence-vectors@v0.11.1"),
    ("an action reference", f"uses: {OWNER}/agent-evidence-vectors@v0.11.1"),
    # Every shape below was refused until the bare word stopped being a rule.
    # None of them is a path to the website, so none of them is a finding.
    ("the bare word alone", f"built by {COMPANY} in 2026"),
    ("the bare word capitalised", f"{COMPANY.title()} evidence tooling"),
    ("the bare word beside a repository path", f"{OWNER}/agent-evidence-vectors run by {COMPANY}"),
    ("the organization name", f"Both are maintained by {ORG_NAME}."),
    ("the verifier repository", f"https://github.com/{OWNER}/{VERIFIER_REPO}"),
    ("the verifier command variable", f"{VERIFIER_ENV}: uv run {VERIFIER_REPO}"),
    ("a policy schema string", f'"schema": "{POLICY_SCHEMA}"'),
    ("a case schema string", f'"schema": "{CASE_SCHEMA}"'),
    ("the organisation handle alone", f"maintainer of the {OWNER} organisation"),
    ("the handle ending a sentence", f"the owner is {OWNER}."),
    ("the organisation page", f"https://github.com/{OWNER}"),
    ("a repository the permit does not list", f"https://github.com/{OWNER}/some-future-repo"),
)

REFUSED = (
    ("the website in a sentence", f"see {SITE} for more"),
    ("the website inside a link", f"[docs](https://{SITE}/predicate/v1/)"),
    ("the website bare", SITE),
    ("the website in capitals", SITE.upper()),
    ("the website on a subdomain", f"https://docs.{SITE}/start"),
    ("the website name without its suffix", f"@{SITE.split('.')[0]} on social media"),
    ("the website beside a repository path", f"{OWNER}/agent-evidence-vectors, see {SITE}"),
    ("the website beside the bare word", f"{COMPANY.title()} docs live at {SITE}"),
    ("the website name glued to the organization name", f"Get{ORG_NAME} maintains this"),
    # The host with its first letters written as an escape. The bare word used
    # to catch these by accident; the host's own tail has to catch them now.
    ("the website with its first letter JSON-escaped", f"https://{ESCAPED_JSON_HOST}/x"),
    ("the website with its first letter as an HTML entity", f"see {ESCAPED_HTML_HOST}"),
    ("another first-party product", f"the {OTHER} runtime"),
    ("another first-party product as an identifier", f"{OTHER.upper()}_EOF"),
)

# The private-path rules live in the history scanner alone. The content scanner
# and the commit-message gate rule on the salted words, so these are asserted
# where they are enforced.
HISTORY_REFUSED = (
    ("an absolute home path", f"see {HOME_PATH}"),
    ("a private dossier name", f"see {DOSSIER_PATH}/notes.md"),
    ("a private product name only the history scanner lists", f"the {THIRD_PRODUCT} runner"),
)


def _pattern_cases() -> tuple[int, list[str]]:
    """Pin the history scanner's own word list, apart from the salted sidecar.

    The history scanner refuses a line when either its own pattern list or the
    salted sidecar fires, so a case run through the whole scanner cannot tell
    whether the list still holds a word the sidecar also holds. Measured: with
    the website name, the host's tail or the other product deleted from the
    list, every case above still held. These cases read the list alone.
    """
    bad: list[str] = []
    ran = 0
    names = [(w, l) for w, l in REFUSED] + [HISTORY_REFUSED[-1]]
    for what, line in names:
        ran += 1
        if scan.IDENTITY.search(scan.permit(line)):
            print(f"ok   refused    {what} (history scanner's own list)")
        else:
            bad.append(f"{what} (history scanner's own list): PASSED, the list lost a word")
    for what, line in PERMITTED:
        ran += 1
        if scan.IDENTITY.search(scan.permit(line)):
            bad.append(f"{what} (history scanner's own list): refused, but this shape is not a finding")
        else:
            print(f"ok   permitted  {what} (history scanner's own list)")
    return ran, bad


# The sibling scanner. `forbidden-word-scan.py` reads tracked CONTENT where the
# hook above reads pushed HISTORY, and the two share one rule file, so they need
# the same rules or the repository passes one guard and fails the other. It is
# exercised through a file because that is its only input. Where a repository
# does not carry it, these cases report as skipped and never as passed.
CONTENT_SCANNER = HERE / "forbidden-word-scan.py"


def content_refuses(line: str) -> bool:
    """Whether the content scanner refuses a file containing `line`."""
    with tempfile.TemporaryDirectory() as raw:
        probe = Path(raw) / "probe.txt"
        probe.write_text(line + "\n", encoding="utf-8")
        done = subprocess.run(
            [sys.executable, str(CONTENT_SCANNER), str(probe)],
            capture_output=True, text=True, timeout=180, check=False,
        )
    return done.returncode != 0


# The commit-message gate reads the same salted sidecar. It is exercised
# through a message file because that is its contract with git, and every case
# rides in the BODY under a fixed clean subject, so a refusal is attributable to
# the line under test and not to the subject-length rule. `_hook_control`
# asserts that the fixed message passes on its own.
HOOK = HERE.parent / ".githooks" / "commit-msg"
HOOK_SUBJECT = "chore: probe the identity rules"


def _hook(body: str) -> int:
    with tempfile.TemporaryDirectory() as raw:
        message = Path(raw) / "COMMIT_EDITMSG"
        message.write_text(f"{HOOK_SUBJECT}\n\n{body}\n", encoding="utf-8")
        done = subprocess.run(
            [sys.executable, str(HOOK), str(message)],
            capture_output=True, text=True, timeout=180, check=False,
        )
        return done.returncode


def hook_refuses(line: str) -> bool:
    """Whether the commit-message gate refuses a message whose body is `line`."""
    return _hook(line) != 0


def _run_cases(
    refuses: Callable[[str], bool],
    permitted: Sequence[tuple[str, str]],
    refused_cases: Sequence[tuple[str, str]],
    label: str,
) -> tuple[int, list[str]]:
    """Run one guard over both populations; return the count that RAN and the failures."""
    bad: list[str] = []
    ran = 0
    for what, line in permitted:
        ran += 1
        if refuses(line):
            bad.append(f"{what}{label}: refused, but this shape is not a finding")
        else:
            print(f"ok   permitted  {what}{label}")
    for what, line in refused_cases:
        ran += 1
        if refuses(line):
            print(f"ok   refused    {what}{label}")
        else:
            bad.append(f"{what}{label}: PASSED, so the guard no longer refuses it")
    return ran, bad


def main() -> int:
    total, failures = _run_cases(refused, PERMITTED, REFUSED + HISTORY_REFUSED, "")
    more, bad = _pattern_cases()
    total += more
    failures += bad
    if CONTENT_SCANNER.exists():
        more, bad = _run_cases(content_refuses, PERMITTED, REFUSED, " (content scanner)")
        total += more
        failures += bad
    else:
        print("skip content scanner: this repository does not carry one")
    if HOOK.exists():
        total += 1
        if _hook("a body that names nothing at all") != 0:
            failures.append(
                "the commit-message harness failed its own control: a message naming "
                "nothing was refused, so every hook case would be meaningless"
            )
        else:
            more, bad = _run_cases(hook_refuses, PERMITTED, REFUSED, " (commit-message gate)")
            total += more
            failures += bad
    else:
        print("skip commit-message gate: this repository does not carry one")
    for line in failures:
        print(f"FAIL {line}", file=sys.stderr)
    print(f"{total - len(failures)}/{total} cases held")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
