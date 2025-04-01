"""Chat page."""

import logging

from prettyqt import widgets

from chatly.core.translate import _


logger = logging.getLogger(__name__)


class ChatPage(widgets.MainWindow):
    def __init__(self, parent=None):
        """Container widget including a toolbar."""
        super().__init__(parent=parent)
        self.set_object_name("chat_view")
        self.set_title(_("Chat"))
        self.set_icon("mdi.chat")
        widget = widgets.Widget()
        widget.set_layout("vertical", margin=0)
        self.set_widget(widget)


if __name__ == "__main__":
    app = widgets.app()
    w = ChatPage()
    w.show()
    app.main_loop()
