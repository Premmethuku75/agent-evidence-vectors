#!/usr/bin/env python3
"""Validate every file in crosswalk/ against vocabulary.yaml.

Design constraint, stated explicitly because it is the reason this script
exists: a validator that silently skips a file it doesn't recognize is worse
than no validator, because a filed crosswalk in the wrong shape then reads as
correct in the published matrix while actually being invisible. Every file in
crosswalk/ (except TEMPLATE.yaml) MUST either pass validation or fail loudly
with a nonzero exit code. There is no third, silent outcome.

Run: python3 scripts/validate_crosswalks.py
Exit 0: every crosswalk file is valid.
Exit 1: at least one crosswalk file failed validation; see stderr for which
        file and which check.
"""

import sys
import urllib.request
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
VOCAB_PATH = REPO_ROOT / "vocabulary.yaml"
CROSSWALK_DIR = REPO_ROOT / "crosswalk"

MATCH_TYPES = {
    "exact",
    "structural",
    "partial",
    "non_equivalent_similar_label",
    "no_mapping",
}
EVIDENCE_STATES = {"emitted", "inferred", "asserted"}
REQUIRED_MATCH_EVIDENCE = {"exact", "structural", "partial"}
TERM_SECTIONS = (
    "evidence_dimensions",
    "posture_and_coverage",
    "outcome_lattice",
)
REQUIRED_TOP_LEVEL = ("system", "system_url", "crosswalk_version", "vocabulary_version_targeted")


def load_known_terms():
    with open(VOCAB_PATH) as f:
        vocab = yaml.safe_load(f)
    known_terms = {}
    for section in TERM_SECTIONS:
        for term_name in vocab.get(section, {}):
            known_terms[term_name] = section
    return known_terms


def fail(filename, message, errors):
    errors.append(f"{filename}: {message}")


def check_source_path_url(source_path, filename, term_name, warnings):
    """Best-effort resolvability check. A non-URL source_path (e.g. a bare
    repo-relative file path) cannot be fetched here and is not a validator
    failure -- it is flagged for the human reviewer instead, per
    GOVERNANCE.md: the validator does not replace the fetch-and-confirm
    review step for anything non-public."""
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


def validate_crosswalk_file(path, known_terms, errors, warnings):
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
            if match not in MATCH_TYPES:
                fail(
                    filename,
                    f"term '{term_name}' has match='{match}', which is not one of "
                    f"the five registered crosswalk_match_types: {sorted(MATCH_TYPES)}",
                    errors,
                )
                continue
            if match in REQUIRED_MATCH_EVIDENCE:
                evidence = entry.get("evidence")
                if evidence not in EVIDENCE_STATES:
                    fail(
                        filename,
                        f"term '{term_name}' has match='{match}' and therefore MUST "
                        f"declare evidence: one of {sorted(EVIDENCE_STATES)} (got "
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
            "posture_and_coverage / outcome_lattice) -- this file will not "
            "render in the published matrix. If this is intentional (a "
            "system_attributes-only filing), that is currently unsupported; "
            "open an issue rather than filing an invisible crosswalk.",
            errors,
        )


def main():
    if not VOCAB_PATH.exists():
        print(f"FATAL: {VOCAB_PATH} not found", file=sys.stderr)
        return 1

    known_terms = load_known_terms()

    errors = []
    warnings = []
    files = sorted(p for p in CROSSWALK_DIR.glob("*.yaml") if p.name != "TEMPLATE.yaml")

    if not files:
        print("No crosswalk files to validate (crosswalk/ is empty besides TEMPLATE.yaml).")
        return 0

    for path in files:
        validate_crosswalk_file(path, known_terms, errors, warnings)

    for w in warnings:
        print(f"WARNING: {w}", file=sys.stderr)
    for e in errors:
        print(f"ERROR: {e}", file=sys.stderr)

    print(f"\nValidated {len(files)} crosswalk file(s): {len(errors)} error(s), {len(warnings)} warning(s).")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
