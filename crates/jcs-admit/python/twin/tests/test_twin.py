"""The twin is probityai.jcs under the crate's name, and its version is the crate's."""

from __future__ import annotations

from importlib.metadata import requires, version

import jcs_admit
import probityai.jcs


def test_every_name_is_the_same_object_as_in_probityai_jcs():
    assert jcs_admit.__all__ == probityai.jcs.__all__
    for name in jcs_admit.__all__:
        assert getattr(jcs_admit, name) is getattr(probityai.jcs, name), name


def test_the_twin_version_is_the_crate_version_the_binding_links():
    assert jcs_admit.__version__ == jcs_admit.JCS_ADMIT_VERSION


def test_the_twin_pins_the_installed_probityai_exactly():
    assert requires("jcs-admit") == [f"probityai=={version('probityai')}"]


def test_it_works():
    assert jcs_admit.admit(b'{"b":1,"a":2}') == b'{"a":2,"b":1}'
