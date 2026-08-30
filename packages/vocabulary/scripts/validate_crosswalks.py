#!/usr/bin/env python3
"""Validate every file in crosswalk/ against vocabulary.yaml.

Design constraint, stated explicitly because it is the reason this script
exists: a validator that silently skips a file it doesn't recognize is worse
than no validator, because a filed crosswalk in the wrong shape then reads as
correct to anyone reading the directory while contributing nothing. Every file in
crosswalk/ (except TEMPLATE.yaml) MUST either pass validation or fail loudly
with a nonzero exit code. There is no third, silent outcome.

Run: python3 scripts/validate_crosswalks.py
Exit 0: every crosswalk file is valid.
Exit 1: at least one crosswalk file failed validation; see stderr for which
        file and which check.
Exit 2: the run could not happen. The registry is unreadable or one of its
        closed vocabularies is missing, so NOTHING was checked. This is kept
        distinct from exit 1 on purpose: a check that failed and a check that
        never ran are different states, and collapsing them lets a broken
        checker be read as a strict one.
"""

import os
import sys
import urllib.request
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
VOCAB_PATH = REPO_ROOT / "vocabulary.yaml"
CROSSWALK_DIR = REPO_ROOT / "crosswalk"

REQUIRED_MATCH_EVIDENCE = {"exact", "structural", "partial"}
TERM_SECTIONS = (
    "evidence_dimensions",
    "posture_and_coverage",
    "outcome_lattice",
)
REQUIRED_TOP_LEVEL = ("system", "system_url", "crosswalk_version", "vocabulary_version_targeted")

#: Required keys whose VALUE must be a plain scalar, not a mapping or a list.
#:
#: CONTRIBUTING.md has told filers "`system` is a plain string, not a block" since
#: 2026-08-30, and nothing enforced it: a crosswalk with `system:` written as a
#: block validated at zero errors. The rule was right and unbacked, which is the
#: same shape as the defect that sentence was written to describe. A stated rule
#: nothing checks is worse than no rule, because a filer who follows it gets no
#: confirmation and a filer who ignores it gets no refusal.
_SCALAR_TOP_LEVEL = ("system", "system_url", "crosswalk_version", "vocabulary_version_targeted")

#: The two enumerations are READ from the registry, never restated here.
#:
#: They used to be literal sets in this file, and a stray `definition:` key sat
#: as a fourth sibling under `crosswalk_evidence_states` for the whole of
#: 0.1.0 without anything noticing. A consumer enumerating that mapping saw four
#: registered states; this validator saw the three it had been told about, and
#: the two answers never had to agree. `out_of_scope` says a verifier MUST reject
#: an unregistered enum value, so the registry was publishing one against its own
#: rule and its own checker could not see it.
#:
#: A checker that restates the thing it checks can only ever verify that somebody
#: typed the same words twice. So the sets below come from the file, and a
#: registry edit that adds or removes a member reaches this validator on the next
#: run with nobody remembering to mirror it.
_MIN_MEMBERS = 2


def _enum_from(vocab, key):
    """The registered members of one closed vocabulary, read from the registry.

    Refuses; it does not guess. A missing or tiny enumeration means the registry
    is malformed or this validator is pointed at the wrong file, and an empty set
    would silently accept every value a crosswalk could name, which is the exact
    inversion of what this function is for."""
    members = vocab.get(key)
    if not isinstance(members, dict):
        print(
            f"validate_crosswalks: REFUSED -- vocabulary.yaml has no mapping at "
            f"'{key}', so the registered members cannot be read. Nothing was "
            f"validated. This is a broken run, never a clean one.",
            file=sys.stderr,
        )
        raise SystemExit(2)
    if len(members) < _MIN_MEMBERS:
        print(
            f"validate_crosswalks: REFUSED -- '{key}' carries {len(members)} "
            f"member(s), fewer than the {_MIN_MEMBERS} any closed vocabulary "
            f"needs to be worth checking against. Nothing was validated.",
            file=sys.stderr,
        )
        raise SystemExit(2)
    return set(members)


def load_registry():
    """Known terms and both closed vocabularies, all from vocabulary.yaml."""
    with open(VOCAB_PATH) as f:
        vocab = yaml.safe_load(f)
    known_terms = {}
    for section in TERM_SECTIONS:
        for term_name in vocab.get(section, {}):
            known_terms[term_name] = section
    return (
        known_terms,
        _enum_from(vocab, "crosswalk_match_types"),
        _enum_from(vocab, "crosswalk_evidence_states"),
    )


def fail(filename, message, errors):
    errors.append(f"{filename}: {message}")


def check_source_path_url(source_path, filename, term_name, warnings):
    """Best-effort resolvability check. A non-URL source_path (e.g. a bare
    repo-relative file path) cannot be fetched here and is not a validator
    failure -- it is flagged for the human reviewer, per GOVERNANCE.md: the
    validator does not replace the fetch-and-confirm review step for anything
    non-public.

    THIS FUNCTION IS THE ONE PLACE THIS REPOSITORY TOUCHES THE NETWORK, and it is
    why `VALIDATE_CROSSWALKS_OFFLINE` exists. The workflow header called both its
    gates hermetic while every CI run issued a live HEAD request, because the
    contribution guide's worked example carries an https source_path and the test
    that runs that example hands it straight to this check. Nobody wrote a network
    call into CI; one arrived through an example.

    Offline mode records the skip as a WARNING naming what went unchecked. It
    never reports a skipped check as a clean one, which is the whole reason it
    prints anything at all."""
    if os.environ.get("VALIDATE_CROSSWALKS_OFFLINE"):
        warnings.append(
            f"{filename}: term '{term_name}' source_path '{source_path}' was NOT "
            f"checked for resolvability, because this run is offline. That is a "
            f"check that did not happen, never a check that passed."
        )
        return
    if not source_path.startswith(("http://", "https://")):
        warnings.append(
            f"{filename}: term '{term_name}' source_path '{source_path}' is not a "
            f"fetchable URL -- human reviewer must confirm this resolves in the "
            f"filer's own real artifact before merge."
        )
        return
    try:
        req = urllib.request.Request(source_path, method="HEAD")
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        warnings.append(
            f"{filename}: term '{term_name}' source_path '{source_path}' did not "
            f"resolve on a HEAD request ({e}) -- human reviewer must confirm before merge."
        )


def validate_crosswalk_file(path, known_terms, match_types, evidence_states, errors, warnings):
    filename = path.name
    try:
        with open(path) as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        fail(filename, f"not valid YAML: {e}", errors)
        return

    if not isinstance(data, dict):
        fail(filename, "top level must be a mapping, not a list or scalar", errors)
        return

    for key in REQUIRED_TOP_LEVEL:
        if key not in data:
            fail(filename, f"missing required top-level key '{key}'", errors)

    for key in _SCALAR_TOP_LEVEL:
        if key in data and isinstance(data[key], (dict, list)):
            shape = "a block" if isinstance(data[key], dict) else "a list"
            fail(
                filename,
                f"top-level key '{key}' is {shape}; it must be a plain string. "
                f"See the worked example in CONTRIBUTING.md, which this repository "
                f"runs through this validator on every push.",
                errors,
            )

    saw_any_term_section = False
    for section in TERM_SECTIONS + ("system_attributes",):
        if section not in data:
            continue
        block = data[section]
        if not isinstance(block, dict):
            fail(filename, f"section '{section}' must be a mapping of term_name -> details", errors)
            continue
        if section == "system_attributes":
            continue  # declared values, not match-typed terms
        saw_any_term_section = True
        for term_name, entry in block.items():
            if term_name not in known_terms:
                fail(
                    filename,
                    f"term '{term_name}' under '{section}' is not in vocabulary.yaml "
                    f"-- propose it via an issue first (see CONTRIBUTING.md)",
                    errors,
                )
                continue
            if known_terms[term_name] != section:
                fail(
                    filename,
                    f"term '{term_name}' is registered under "
                    f"'{known_terms[term_name]}' in vocabulary.yaml, not '{section}'",
                    errors,
                )
            if not isinstance(entry, dict) or "match" not in entry:
                fail(
                    filename,
                    f"term '{term_name}' entry must be a mapping with a 'match' key "
                    f"(not e.g. a bare 'mapping:' list or an unlabelled value)",
                    errors,
                )
                continue
            match = entry["match"]
            if match not in match_types:
                fail(
                    filename,
                    f"term '{term_name}' has match='{match}', which is not one of "
                    f"the registered crosswalk_match_types: {sorted(match_types)}",
                    errors,
                )
                continue
            if match in REQUIRED_MATCH_EVIDENCE:
                evidence = entry.get("evidence")
                if evidence not in evidence_states:
                    fail(
                        filename,
                        f"term '{term_name}' has match='{match}' and therefore MUST "
                        f"declare evidence: one of {sorted(evidence_states)} (got "
                        f"'{evidence}')",
                        errors,
                    )
                source_path = entry.get("source_path")
                if not source_path:
                    fail(
                        filename,
                        f"term '{term_name}' has match='{match}' and therefore MUST "
                        f"declare a source_path",
                        errors,
                    )
                elif evidence == "emitted":
                    check_source_path_url(source_path, filename, term_name, warnings)
                if match == "partial" and not entry.get("divergences"):
                    fail(
                        filename,
                        f"term '{term_name}' has match='partial' and therefore MUST "
                        f"list at least one item under divergences",
                        errors,
                    )

    if not saw_any_term_section:
        fail(
            filename,
            "no recognized term section found (evidence_dimensions / "
            "posture_and_coverage / outcome_lattice) -- this file maps no term, "
            "so nothing reading the registry would see it. If that is "
            "intentional (a system_attributes-only filing), it is currently "
            "unsupported; open an issue.",
            errors,
        )


def main():
    if not VOCAB_PATH.exists():
        print(f"FATAL: {VOCAB_PATH} not found", file=sys.stderr)
        return 1

    known_terms, match_types, evidence_states = load_registry()

    errors = []
    warnings = []
    files = sorted(p for p in CROSSWALK_DIR.glob("*.yaml") if p.name != "TEMPLATE.yaml")

    if not files:
        print("No crosswalk files to validate (crosswalk/ is empty besides TEMPLATE.yaml).")
        return 0

    for path in files:
        validate_crosswalk_file(
            path, known_terms, match_types, evidence_states, errors, warnings
        )

    for w in warnings:
        print(f"WARNING: {w}", file=sys.stderr)
    for e in errors:
        print(f"ERROR: {e}", file=sys.stderr)

    print(f"\nValidated {len(files)} crosswalk file(s): {len(errors)} error(s), {len(warnings)} warning(s).")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
