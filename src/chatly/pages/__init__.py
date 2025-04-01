from __future__ import annotations

from chatly.pages.settings_page import SettingsPage
from chatly.pages.ocr_page import OcrPage
from chatly.pages.start_page import StartPage
from chatly.pages.chat_page import ChatPage
from chatly.pages.browser_page import HelpPage

# from chatly.pages.explorer_page import FileExplorerPage
from chatly.pages.log_page import LogPage

__all__ = [
    "ChatPage",
    # "FileExplorerPage",
    "HelpPage",
    "LogPage",
    "OcrPage",
    "SettingsPage",
    "StartPage",
]
