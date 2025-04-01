"""Start page."""

import logging

from prettyqt import core, widgets

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

        # Main widget
        widget = widgets.Widget()
        widget.set_layout("vertical", margin=0)
        self.set_widget(widget)

        # Create a splitter to divide the view
        splitter = widgets.Splitter(orientation="horizontal")
        widget.box.add(splitter)

        # File explorer on the left
        self.file_explorer = self.create_file_explorer()
        splitter.add(self.file_explorer)

        # File preview on the right using WebEngineView for all content
        self.preview_widget = PreviewWidget()
        splitter.add(self.preview_widget)

        # Set initial sizes (30% left, 70% right)
        splitter.set_sizes([300, 700])

    def create_file_explorer(self):
        """Create a file explorer view."""
        widget = widgets.Widget()
        widget.set_layout("vertical")

        # Label
        label = widgets.Label(_("Files"))
        label.set_bold()
        widget.box.add(label)
        home_dir = str(core.Dir.home())

        # File system model and tree view
        self.fs_model = widgets.FileSystemModel()
        self.fs_model.set_root_path(home_dir)
        # Show both PDFs and common image formats
        self.fs_model.set_name_filters([
            "*.pdf",
            "*.jpg",
            "*.jpeg",
            "*.png",
            "*.bmp",
            "*.gif",
        ])
        self.fs_model.set_name_filter_disables(False)

        self.tree_view = widgets.TreeView()
        self.tree_view.set_model(self.fs_model)

        # Show only the filename column
        for i in range(1, self.fs_model.columnCount()):
            self.tree_view.hide_column(i)

        # Connect selection to display file
        self.tree_view.double_clicked.connect(self.on_file_selected)

        widget.box.add(self.tree_view)
        return widget

    def on_file_selected(self, index):
        """Handle file selection in the explorer."""
        file_path = self.fs_model.get_file_path(index)
        if file_path.is_file():
            # Load file in the preview widget
            self.preview_widget.load_file(file_path)


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    app = widgets.app()
    w = StartPage()
    w.show()
    app.main_loop()
