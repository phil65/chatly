"""Chat page."""

import logging

from prettyqt import widgets


logger = logging.getLogger(__name__)


class ChatPage(widgets.MainWindow):
    def __init__(self, parent=None):
        """Container widget including a toolbar."""
        super().__init__(
            parent=parent,
            object_name="chat_view",
            window_title="Chat",
            window_icon="mdi.chat",
        )
        widget = widgets.Widget()
        widget.set_layout("vertical", margin=0)
        self.set_widget(widget)


if __name__ == "__main__":
    app = widgets.app()
    w = ChatPage()
    w.show()
    app.main_loop()
