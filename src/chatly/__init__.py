from __future__ import annotations

from importlib.metadata import version

__version__ = version("chatly")
__title__ = "Chatly"

from chatly.application import MainApp

__all__ = ["MainApp", "__title__", "__version__"]
