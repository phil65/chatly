from __future__ import annotations

import logging
import sys

from prettyqt import core, widgets

import chatly


logger = logging.getLogger(__name__)


class MainApp(widgets.Application):
    popup_info = core.Signal(str)
    settings_updated = core.Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(sys.argv)
        self.set_metadata(app_name=chatly.__title__, app_version=chatly.__version__)
