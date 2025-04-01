"""OCR page."""

import logging

from prettyqt import widgets

from chatly.core.translate import _


logger = logging.getLogger(__name__)


class OcrPage(widgets.MainWindow):
    def __init__(self, parent=None):
        """Container widget including a toolbar."""
        super().__init__(parent=parent)
        self.set_object_name("ocr_view")
        self.set_title(_("OCR"))
        self.set_icon("mdi.file-document-outline")
        widget = widgets.Widget()
        widget.set_layout("vertical", margin=0)
        self.set_widget(widget)


if __name__ == "__main__":
    app = widgets.app()
    w = OcrPage()
    w.show()
    app.main_loop()
