#!/usr/bin/env python3
"""Verify the built Python files before PyPI publication, then lay out one upload directory per project.

    check-python-release.py DIST --tag py-v0.1.0 --project probityai --out UPLOAD

DIST holds every file the python workflow built. The check refuses unless the tag names
the version in python/pyproject.toml, the file set is exactly the expected population
(seven probityai wheels, its sdist, the jcs-admit twin's wheel and sdist, nothing else),
every wheel and sdist carries the project's name and version in its own metadata, and the
twin requires exactly that probityai release. It copies the chosen project's files to OUT.
"""
import argparse
import re
import shutil
import sys
import tarfile
import tomllib
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLATFORMS = (
    "manylinux_2_28_x86_64",
    "manylinux_2_28_aarch64",
    "musllinux_1_2_x86_64",
    "musllinux_1_2_aarch64",
    "macosx_",  # two files, told apart below
    "win_amd64",
)


def need(condition, message):
    if not condition:
        raise SystemExit("check-python-release: " + message)


def project(path):
    return tomllib.loads((ROOT / path).read_text())["project"]


def metadata(path):
    """Return the core metadata text of a wheel or an sdist."""
    if path.suffix == ".whl":
        with zipfile.ZipFile(path) as wheel:
            names = [n for n in wheel.namelist() if re.fullmatch(r"[^/]+\.dist-info/METADATA", n)]
            need(len(names) == 1, f"{path.name}: expected one METADATA, found {names}")
            return wheel.read(names[0]).decode()
    with tarfile.open(path) as sdist:
        names = [n for n in sdist.getnames() if n.count("/") == 1 and n.endswith("/PKG-INFO")]
        need(len(names) == 1, f"{path.name}: expected one PKG-INFO, found {names}")
        return sdist.extractfile(names[0]).read().decode()


def field(text, name):
    return [m.group(1).strip() for m in re.finditer(rf"^{name}: (.*)$", text, re.M)]


def plan(dist, binding, twin):
    """Map each expected file name to its project name and version."""
    files = {p.name: p for p in dist.iterdir()}
    pv, tv = binding["version"], twin["version"]
    expected = {f"probityai-{pv}.tar.gz": "probityai"}
    expected[f"jcs_admit-{tv}-py3-none-any.whl"] = "jcs-admit"
    expected[f"jcs_admit-{tv}.tar.gz"] = "jcs-admit"
    wheels = [n for n in files if n.startswith(f"probityai-{pv}-cp310-abi3-") and n.endswith(".whl")]
    for family in PLATFORMS:
        hits = [n for n in wheels if family in n]
        need(len(hits) == (2 if family == "macosx_" else 1), f"wheels for {family}: {hits}")
        expected.update({n: "probityai" for n in hits})
    need(files.keys() == expected.keys(), f"file set differs: extra {sorted(files.keys() - expected.keys())}, missing {sorted(expected.keys() - files.keys())}")
    return files, expected


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dist", type=Path)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--project", choices=("probityai", "jcs-admit"), required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args(argv)

    binding, twin = project("python/pyproject.toml"), project("python/twin/pyproject.toml")
    need(binding["name"] == "probityai" and twin["name"] == "jcs-admit", "project names changed")
    need(args.tag == "py-v" + binding["version"], f"tag {args.tag} is not py-v{binding['version']}")
    need(twin["dependencies"] == [f"probityai=={binding['version']}"], f"twin dependencies {twin['dependencies']}")
    files, expected = plan(args.dist, binding, twin)

    versions = {"probityai": binding["version"], "jcs-admit": twin["version"]}
    for name, owner in expected.items():
        text = metadata(files[name])
        need(field(text, "Name") == [owner], f"{name}: Name {field(text, 'Name')}")
        need(field(text, "Version") == [versions[owner]], f"{name}: Version {field(text, 'Version')}")
        if owner == "jcs-admit":
            need(field(text, "Requires-Dist") == [f"probityai=={binding['version']}"], f"{name}: Requires-Dist {field(text, 'Requires-Dist')}")

    args.out.mkdir(parents=True, exist_ok=True)
    need(not any(args.out.iterdir()), f"{args.out} is not empty")
    chosen = sorted(n for n, owner in expected.items() if owner == args.project)
    for name in chosen:
        shutil.copy2(files[name], args.out / name)
    print(f"{args.project} {versions[args.project]}: {len(chosen)} files verified and staged in {args.out}")
    for name in chosen:
        print("  " + name)


if __name__ == "__main__":
    main(sys.argv[1:])
