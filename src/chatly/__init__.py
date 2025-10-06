"""Chatly: Agent desktop app"""

from __future__ import annotations

from importlib.metadata import version

__version__ = version("chatly")
__title__ = "Chatly"
__description__ = "Agent desktop app"
__author__ = "Philipp Temminghoff"
__author_email__ = "philipptemminghoff@googlemail.com"
__copyright__ = "Copyright (c) 2025 Philipp Temminghoff"
__license__ = "MIT"
__url__ = "https://github.com/phil65/chatly"


from chatly.application import MainApp

__all__ = ["MainApp", "__title__", "__version__"]
