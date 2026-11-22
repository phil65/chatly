"""Smoke test: the package imports and reports its version."""

from __future__ import annotations

import chatly


def test_package_imports() -> None:
    """The package can be imported and exposes a version string."""
    assert isinstance(chatly.__version__, str)
