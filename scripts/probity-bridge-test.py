#!/usr/bin/env python3
"""The Probity bridge line is in the Action summary and in every spec README.

Ruling P-54 puts one line on every spec README and on the Action's job summary:
"Verified by Probity" with the link to the offline verifier and its pinned
install. This test holds each copy to `BRIDGE` in scripts/action-summary.py:

1. A passing run's summary carries the line once, after the result table.
2. A failing run's summary does not carry it, because the line says "Verified".
3. Every vectors-*/README.md that exists, and spec/README.md, carries it.
4. Removing the line from the summary script turns check 1 red, so the check
   cannot pass while the summary has lost the line.

Run with: python3 scripts/probity-bridge-test.py
"""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent
SUMMARY = HERE / "action-summary.py"

_spec = importlib.util.spec_from_file_location("action_summary", SUMMARY)
assert _spec is not None and _spec.loader is not None
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)
BRIDGE: str = _module.BRIDGE

REPORT = {
    "rail": "external",
    "railNote": "synthetic",
    "totals": {"vectors": 3, "pass": 3, "fail": 0, "conform": 3,
               "reasonParityMismatch": 0, "suiteRefusals": 0},
    "vectors": [],
    "verifier": {"command": "x", "vectorsExecuted": 3},
}


def run_summary(script: Path, status: str, work: Path) -> str:
    report = work / "report.json"
    report.write_text(json.dumps(REPORT), encoding="utf-8")
    summary = work / "summary.md"
    summary.write_text("", encoding="utf-8")
    outputs = work / "outputs.txt"
    outputs.write_text("", encoding="utf-8")
    env = dict(os.environ, REPORT=str(report), STATUS=status, CORPUS="vectors",
               GITHUB_STEP_SUMMARY=str(summary), GITHUB_OUTPUT=str(outputs))
    subprocess.run([sys.executable, str(script)], env=env, check=True, capture_output=True)
    return summary.read_text(encoding="utf-8")


def summary_errors(script: Path, work: Path) -> list[str]:
    errors: list[str] = []
    passed = run_summary(script, "0", work)
    if passed.count(BRIDGE) != 1:
        errors.append(f"pass summary carries the bridge {passed.count(BRIDGE)} times, expected 1")
    elif passed.index(BRIDGE) < passed.index("| ---: |"):
        errors.append("pass summary puts the bridge before the result table")
    if BRIDGE in run_summary(script, "1", work):
        errors.append("a failing run's summary says Verified by Probity")
    return errors


def readme_errors() -> list[str]:
    paths = sorted(REPO_ROOT.glob("vectors-*/README.md")) + [REPO_ROOT / "spec" / "README.md"]
    return [
        f"{p.relative_to(REPO_ROOT)} lacks the bridge line; the text is BRIDGE in "
        "scripts/action-summary.py"
        for p in paths
        if BRIDGE not in p.read_text(encoding="utf-8")
    ]


def mutation_errors(work: Path) -> list[str]:
    source = SUMMARY.read_text(encoding="utf-8")
    anchor = 'summary.append(f"{BRIDGE}\\n\\n")'
    if source.count(anchor) != 1:
        return ["mutation: the bridge append is not present exactly once; it would prove nothing"]
    mutant = work / "action-summary-mutant.py"
    mutant.write_text(source.replace(anchor, "pass"), encoding="utf-8")
    if not summary_errors(mutant, work):
        return ["mutation: the summary check stayed GREEN with the bridge line removed"]
    return []


def main() -> int:
    errors: list[str] = []
    with tempfile.TemporaryDirectory(prefix="aev-bridge-") as tmp:
        work = Path(tmp)
        errors += summary_errors(SUMMARY, work)
        errors += mutation_errors(work)
    errors += readme_errors()
    if errors:
        print(f"FAIL: the Probity bridge line ({len(errors)}):", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1
    print("OK: the Action summary and every spec README carry the Probity bridge line, "
          "and removing it from the summary turns this test red.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
