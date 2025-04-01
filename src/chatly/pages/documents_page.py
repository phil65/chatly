"""Documents page."""

from __future__ import annotations

import logging

from prettyqt import core, widgets

from chatly.core.document_manager import DocumentManager
from chatly.core.translate import _
from chatly.widgets.preview_widget import PreviewWidget


logger = logging.getLogger(__name__)


class DocumentsPage(widgets.MainWindow):
    def __init__(self, parent=None):
        """Container widget including a toolbar."""
        super().__init__(parent=parent)
        self.set_object_name("documents_view")
        self.set_title(_("Documents"))
        self.set_icon("mdi.file-document-outline")
        self.document_manager = DocumentManager.instance()

        # Main widget
        main_widget = widgets.Widget()
        main_widget.set_layout("horizontal", margin=0)
        self.set_widget(main_widget)

        self.splitter = widgets.Splitter(orientation="horizontal")
        main_widget.box.add(self.splitter)
        self.doc_list_widget = self.create_document_list()
        self.splitter.add(self.doc_list_widget)
        self.preview_widget = PreviewWidget()
        self.splitter.add(self.preview_widget)
        self.splitter.set_sizes([300, 700])
        self.document_manager.document_added.connect(self.update_document_list)
        self.document_manager.document_removed.connect(self.update_document_list)

    def create_document_list(self):
        """Create the document list widget."""
        widget = widgets.Widget()
        widget.set_layout("vertical")

        header_layout = widget.box.add_layout("horizontal")
        label = widgets.Label(_("Converted Documents"))
        label.set_bold()
        header_layout.add(label)

        # Add refresh and clear buttons
        btn_refresh = widgets.ToolButton(icon="mdi.refresh")
        btn_refresh.set_tool_tip(_("Refresh document list"))
        btn_refresh.clicked.connect(self.update_document_list)
        header_layout.add_stretch()
        header_layout.add(btn_refresh)

        btn_clear = widgets.ToolButton(icon="mdi.delete")
        btn_clear.set_tool_tip(_("Clear all documents"))
        btn_clear.clicked.connect(self.clear_documents)
        header_layout.add(btn_clear)

        # Document list
        self.list_widget = widgets.ListWidget()
        self.list_widget.set_selection_mode("single")
        self.list_widget.current_item_changed.connect(self.on_document_selected)
        widget.box.add(self.list_widget)

        # Document info panel
        self.info_panel = widgets.GroupBox(_("Document Info"))
        self.info_panel.set_layout("form")
        self.info_title = widgets.Label()
        self.info_converter = widgets.Label()
        self.info_source = widgets.Label()
        self.info_panel.box.add_row(_("Title:"), self.info_title)
        self.info_panel.box.add_row(_("Converter:"), self.info_converter)
        self.info_panel.box.add_row(_("Source:"), self.info_source)
        widget.box.add(self.info_panel)

        # Initially populate the list
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
            item.set_data(core.Qt.ItemDataRole.UserRole, doc_id)
            item.set_data(
                core.Qt.ItemDataRole.ToolTipRole,
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
            # Clear info panel
            self.info_title.set_text("")
            self.info_converter.set_text("")
            self.info_source.set_text("")

    def on_document_selected(self, current, previous):
        """Handle document selection in the list."""
        if not current:
            self.preview_widget.set_default_view()
            # Clear info panel
            self.info_title.set_text("")
            self.info_converter.set_text("")
            self.info_source.set_text("")
            return

        doc_id = current.data(core.Qt.ItemDataRole.UserRole)
        document = self.document_manager.get_document(doc_id)

        if document:
            # Update preview
            self.preview_widget.load_markdown(document.content)

            # Update info panel
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
