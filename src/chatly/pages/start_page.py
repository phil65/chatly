"""Start page."""

import logging
from pathlib import Path
import uuid

import anyenv
from prettyqt import core, widgets

from chatly.core import threads
from chatly.core.converters import CONVERTERS
from chatly.core.document_manager import DocumentManager
from chatly.core.translate import _
from chatly.widgets.preview_widget import PreviewWidget


logger = logging.getLogger(__name__)


class StartPage(widgets.MainWindow):
    def __init__(self, parent=None):
        """Container widget including a toolbar."""
        super().__init__(parent=parent)
        self.set_object_name("start_view")
        self.set_title(_("Start"))
        self.set_icon("mdi.home")
        self.document_manager = DocumentManager.instance()
        self.current_file = None
        widget = widgets.Widget()
        widget.set_layout("vertical", margin=0)
        self.set_widget(widget)
        self.splitter = widgets.Splitter(orientation="horizontal")
        widget.box.add(self.splitter)
        self.file_explorer = self.create_file_explorer()
        self.splitter.add(self.file_explorer)
        self.preview_widget = PreviewWidget()
        self.splitter.add(self.preview_widget)
        self.converter_panel = self.create_converter_panel()
        self.splitter.add(self.converter_panel)
        self.splitter.set_sizes([300, 600, 300])

    def create_file_explorer(self):
        """Create a file explorer view."""
        widget = widgets.Widget()
        widget.set_layout("vertical")
        label = widgets.Label(_("Files"))
        label.set_bold()
        widget.box.add(label)
        home_dir = str(core.Dir.home())
        self.fs_model = widgets.FileSystemModel()
        self.fs_model.set_root_path(home_dir)
        exts = ["*.pdf", "*.jpg", "*.jpeg", "*.png", "*.bmp", "*.gif"]
        self.fs_model.set_name_filters(exts)
        self.fs_model.set_name_filter_disables(False)
        self.tree_view = widgets.TreeView()
        self.tree_view.set_model(self.fs_model)
        for i in range(1, self.fs_model.columnCount()):
            self.tree_view.hide_column(i)
        self.tree_view.h_header.resize_sections("stretch")
        self.tree_view.double_clicked.connect(self.on_file_selected)
        self.tree_view.clicked.connect(self.on_file_selected)
        widget.box.add(self.tree_view)
        return widget

    def create_converter_panel(self):
        """Create a panel with converter buttons."""
        widget = widgets.Widget()
        widget.set_layout("vertical")
        label = widgets.Label(_("Document Converters"))
        label.set_bold()
        widget.box.add(label)
        info_label = widgets.Label(_("Select a file to convert"))
        info_label.set_word_wrap(True)
        widget.box.add(info_label)
        scroll_area = widgets.ScrollArea()
        scroll_area.set_widget_resizable(True)
        button_widget = widgets.Widget()
        button_layout = button_widget.set_layout("vertical")
        self.converter_buttons = {}
        for name in CONVERTERS:
            btn = widgets.PushButton(name)
            btn.set_enabled(False)  # Disabled until a file is selected
            btn.clicked.connect(lambda checked=False, n=name: self.convert_document(n))
            button_layout.add(btn)
            self.converter_buttons[name] = btn
        scroll_area.set_widget(button_widget)
        widget.box.add(scroll_area)
        self.status_label = widgets.Label()
        self.status_label.set_word_wrap(True)
        widget.box.add(self.status_label)

        return widget

    def on_file_selected(self, index):
        """Handle file selection in the explorer."""
        file_path = self.fs_model.get_file_path(index)
        if file_path.is_file():
            self.current_file = file_path
            # Load file in the preview widget
            self.preview_widget.load_file(file_path)
            # Enable converter buttons
            for btn in self.converter_buttons.values():
                btn.set_enabled(True)
            self.status_label.set_text(_("Ready to convert"))

    def convert_document(self, converter_name):
        """Start document conversion in a background thread."""
        if not self.current_file:
            return

        for btn in self.converter_buttons.values():
            btn.set_enabled(False)

        self.status_label.set_text(_("Converting..."))
        worker = threads.Worker(self._run_conversion, converter_name, self.current_file)
        worker.signals.result.connect(self._on_conversion_complete)
        worker.signals.error.connect(self._on_conversion_error)
        msg = _("Converting with {converter}...").format(converter=converter_name)
        threads.pool.start(worker, set_busy=True, message=msg)

    def _run_conversion(self, converter_name, file_path):
        """Run the actual conversion process."""
        converter_cls = CONVERTERS[converter_name]
        converter = converter_cls()
        document = anyenv.run_sync(converter.convert_file(str(file_path)))
        if not document.source_path:
            document.source_path = str(file_path)
        if not document.title:
            document.title = Path(file_path).stem
        doc_id = str(uuid.uuid4())
        return doc_id, document, converter_name

    def _on_conversion_complete(self, result):
        """Handle successful conversion."""
        doc_id, document, con_name = result
        self.document_manager.add_document(doc_id, document, con_name)
        for btn in self.converter_buttons.values():
            btn.set_enabled(True)
        text = _("Conversion successful with {converter}").format(converter=con_name)
        self.status_label.set_text(text)
        # self.preview_widget.load_markdown(document.content)

    def _on_conversion_error(self, error):
        """Handle conversion error."""
        logger.exception("Conversion error", exc_info=error)
        for btn in self.converter_buttons.values():
            btn.set_enabled(self.current_file is not None)
        self.status_label.set_text(_("Error: {error}").format(error=str(error)))


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    app = widgets.app()
    w = StartPage()
    w.show()
    app.main_loop()
