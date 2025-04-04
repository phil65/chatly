"""Documents page with dockable preview and raw text widgets."""

from __future__ import annotations

import logging

from prettyqt import constants, core, widgets

from chatly.core.document_manager import DocumentManager
from chatly.core.translate import _
from chatly.widgets.preview_widget import PreviewWidget


logger = logging.getLogger(__name__)


class DocumentsPage(widgets.MainWindow):
    def __init__(self, parent=None):
        """Container widget including dockable components."""
        super().__init__(
            parent=parent,
            object_name="documents_view",
            window_title="Documents",
            window_icon="mdi.file-document-outline",
        )
        self.document_manager = DocumentManager.instance()
        self.doc_list_widget = self.create_document_list()
        self.set_widget(self.doc_list_widget)
        self.preview_widget = PreviewWidget()
        preview_dock = self.add_dockwidget(self.preview_widget, position="right")
        preview_dock.set_title(_("Document Preview"))
        self.raw_markdown = widgets.PlainTextEdit()
        self.raw_markdown.set_read_only(True)
        self.raw_markdown.set_line_wrap_mode("none")
        # self.raw_markdown.set_font_family("monospace")
        markdown_dock = self.add_dockwidget(self.raw_markdown, "bottom")
        markdown_dock.set_title(_("Raw Markdown"))
        self.document_manager.document_added.connect(self.update_document_list)
        self.document_manager.document_removed.connect(self.update_document_list)

    def create_document_list(self):
        """Create the document list widget."""
        widget = widgets.Widget()
        widget.set_layout("vertical")

        header_layout = widgets.HBoxLayout(parent=widget.box)
        label = widgets.Label(_("Converted Documents"))
        label.set_bold()
        header_layout.add(label)
        btn_refresh = widgets.ToolButton(icon="mdi.refresh")
        btn_refresh.set_tooltip(_("Refresh document list"))
        btn_refresh.clicked.connect(self.update_document_list)
        header_layout.add_stretch()
        header_layout.add(btn_refresh)
        btn_clear = widgets.ToolButton(icon="mdi.delete")
        btn_clear.set_tooltip(_("Clear all documents"))
        btn_clear.clicked.connect(self.clear_documents)
        header_layout.add(btn_clear)

        self.list_widget = widgets.ListWidget()
        self.list_widget.set_selection_mode("single")
        self.list_widget.currentItemChanged.connect(self.on_document_selected)
        widget.box.add(self.list_widget)

        self.info_panel = widgets.GroupBox(_("Document Info"))
        self.info_panel.set_layout("form")
        self.info_title = widgets.Label()
        self.info_converter = widgets.Label()
        self.info_source = widgets.Label()
        self.info_panel.box.add(
            (_("Title:"), self.info_title),
            (_("Converter:"), self.info_converter),
            (_("Source:"), self.info_source),
        )
        widget.box.add(self.info_panel)

        self.update_document_list()
        return widget

    def update_document_list(self, *args, **kwargs):
        """Update the document list from the document manager."""
        self.list_widget.clear()

        documents = self.document_manager.list_documents()
        for doc_id, doc in documents:
            title = doc.title or "Untitled Document"
            converter = self.document_manager.get_converter(doc_id) or "Unknown"
            item = widgets.ListWidgetItem(f"{title} ({converter})")
            item.set_data(constants.USER_ROLE, doc_id)
            item.set_data(
                constants.TOOLTIP_ROLE,
                f"Source: {doc.source_path or 'Unknown'}",
            )
            self.list_widget += item

    def clear_documents(self):
        """Clear all documents after confirmation."""
        if not self.document_manager.list_documents():
            return

        result = widgets.MessageBox.question(
            self,
            _("Clear Documents"),
            _("Are you sure you want to remove all documents?"),
            buttons=widgets.MessageBox.StandardButton.Yes
            | widgets.MessageBox.StandardButton.No,
        )

        if result == widgets.MessageBox.StandardButton.Yes:
            self.document_manager.clear()
            self.preview_widget.set_default_view()
            self.raw_markdown.clear()
            self.info_title.set_text("")
            self.info_converter.set_text("")
            self.info_source.set_text("")

    def on_document_selected(self, current, previous):
        """Handle document selection in the list."""
        if not current:
            self.preview_widget.set_default_view()
            self.raw_markdown.clear()
            # Clear info panel
            self.info_title.set_text("")
            self.info_converter.set_text("")
            self.info_source.set_text("")
            return

        doc_id = current.data(core.Qt.ItemDataRole.UserRole)
        if document := self.document_manager.get_document(doc_id):
            self.preview_widget.load_markdown(document.content)
            self.raw_markdown.set_text(document.content)
            self.info_title.set_text(document.title or "Untitled")
            converter = self.document_manager.get_converter(doc_id) or "Unknown"
            self.info_converter.set_text(converter)
            self.info_source.set_text(str(document.source_path or "Unknown"))


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    app = widgets.app()
    w = DocumentsPage()
    w.show()
    app.main_loop()
