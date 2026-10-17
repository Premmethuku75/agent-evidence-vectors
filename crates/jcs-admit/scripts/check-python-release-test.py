#!/usr/bin/env python3
"""Tests for check-python-release.py: a good file set passes, each fault is refused."""
import importlib.util
import io
import sys
import tarfile
import tempfile
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("check", HERE / "check-python-release.py")
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)

PV = check.project("python/pyproject.toml")["version"]
TV = check.project("python/twin/pyproject.toml")["version"]
WHEELS = [
    "manylinux_2_28_x86_64", "manylinux_2_28_aarch64", "musllinux_1_2_x86_64",
    "musllinux_1_2_aarch64", "macosx_10_12_x86_64", "macosx_11_0_arm64", "win_amd64",
]


def meta(name, version, requires=None):
    text = f"Metadata-Version: 2.4\nName: {name}\nVersion: {version}\n"
    return text + (f"Requires-Dist: {requires}\n" if requires else "")


def wheel(path, name, version, requires=None):
    with zipfile.ZipFile(path, "w") as z:
        z.writestr(f"{name.replace('-', '_')}-{version}.dist-info/METADATA", meta(name, version, requires))


def sdist(path, name, version, requires=None):
    data = meta(name, version, requires).encode()
    with tarfile.open(path, "w:gz") as t:
        info = tarfile.TarInfo(f"{name.replace('-', '_')}-{version}/PKG-INFO")
        info.size = len(data)
        t.addfile(info, io.BytesIO(data))


def build(dist):
    for tag in WHEELS:
        wheel(dist / f"probityai-{PV}-cp310-abi3-{tag}.whl", "probityai", PV)
    sdist(dist / f"probityai-{PV}.tar.gz", "probityai", PV)
    req = f"probityai=={PV}"
    wheel(dist / f"jcs_admit-{TV}-py3-none-any.whl", "jcs-admit", TV, req)
    sdist(dist / f"jcs_admit-{TV}.tar.gz", "jcs-admit", TV, req)


def run(dist, tag, project, out):
    try:
        check.main([str(dist), "--tag", tag, "--project", project, "--out", str(out)])
    except SystemExit as exit_:
        return str(exit_)
    return None


def case(label, mutate, tag=f"py-v{PV}", expect=None):
    with tempfile.TemporaryDirectory() as tmp:
        dist, out = Path(tmp, "dist"), Path(tmp, "out")
        dist.mkdir()
        build(dist)
        mutate(dist)
        err = run(dist, tag, "probityai", out)
        ok = (err is None) if expect is None else (err is not None and expect in err)
        print(("ok   " if ok else "FAIL ") + label + ("" if ok else f": {err}"))
        return ok


def main():
    results = [
        case("a complete set passes", lambda d: None),
        case("a wrong tag is refused", lambda d: None, tag="py-v9.9.9", expect="is not py-v"),
        case("a missing wheel is refused", lambda d: next(d.glob("*win_amd64.whl")).unlink(), expect="win_amd64"),
        case("an extra file is refused", lambda d: (d / "stray.txt").write_text("x"), expect="extra"),
        case("a wrong version inside a wheel is refused",
             lambda d: wheel(next(d.glob("*musllinux_1_2_x86_64.whl")), "probityai", "0.0.1"), expect="Version"),
        case("a twin that requires another release is refused",
             lambda d: wheel(d / f"jcs_admit-{TV}-py3-none-any.whl", "jcs-admit", TV, "probityai==0.0.1"), expect="Requires-Dist"),
    ]
    with tempfile.TemporaryDirectory() as tmp:
        dist, out = Path(tmp, "dist"), Path(tmp, "out")
        dist.mkdir()
        build(dist)
        err = run(dist, f"py-v{PV}", "jcs-admit", out)
        staged = sorted(p.name for p in out.iterdir())
        ok = err is None and staged == sorted([f"jcs_admit-{TV}-py3-none-any.whl", f"jcs_admit-{TV}.tar.gz"])
        print(("ok   " if ok else "FAIL ") + f"the twin upload directory holds only the twin {staged}")
        results.append(ok)
    sys.exit(0 if all(results) else 1)


main()
