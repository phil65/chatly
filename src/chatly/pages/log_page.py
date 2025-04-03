from __future__ import annotations

import logging

from prettyqt import custom_widgets, widgets

from chatly.core.config import config
from chatly.core.translate import _


class LogPage(widgets.Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(parent=kwargs.get("parent"))
        self.set_title(_("Activity log"))
        self.set_icon("mdi.text-subject")
        layout = self.set_layout("horizontal", margin=0)
        self.logwidget = custom_widgets.LogTextEdit()
        toolbar = self.get_toolbar()
        layout.setMenuBar(toolbar)
        layout += self.logwidget
        self.update_settings()

    def get_toolbar(self) -> widgets.ToolBar:
        tb = widgets.ToolBar()
        tb.add_action(
            _("Clear"),
            icon="mdi.notification-clear-all",
            callback=self.logwidget.clear,
        )
        return tb

    def update_settings(self):
        formatter = logging.Formatter(config.log_format)
        self.logwidget.set_formatter(formatter)
        self.logwidget.handler.setLevel(config.log_level)


if __name__ == "__main__":
    app = widgets.app()
    widget = LogPage()
    widget.show()
    app.main_loop()
