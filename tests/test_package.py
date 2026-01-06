from __future__ import annotations

import importlib.metadata

import bmm_tools as m


def test_version():
    assert importlib.metadata.version("bmm_tools") == m.__version__
