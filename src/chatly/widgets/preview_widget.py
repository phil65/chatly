"""Preview widget for documents and images."""

from __future__ import annotations

import logging
import mimetypes
from pathlib import Path

from prettyqt import core, webenginewidgets, widgets

from chatly.core.translate import _


logger = logging.getLogger(__name__)

DEFAULT_HTML = """
    <html>
    <head>
        <style>
            body {
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background-color: #f5f5f5;
                color: #555;
            }
            .message {
                text-align: center;
                padding: 2em;
            }
        </style>
    </head>
    <body>
        <div class="message">
            <h2>Select a file to preview</h2>
            <p>Supported files: PDF, JPG, PNG, JPEG, GIF, BMP</p>
        </div>
    </body>
    </html>
"""

IMAGE_HTML = """
<html>
<head>
    <style>
        body {{
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #f5f5f5;
            height: 100vh;
        }}
        .image-container {{
            max-width: 100%;
            max-height: 100%;
            overflow: auto;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        img {{
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
        }}
    </style>
</head>
<body>
    <div class="image-container">
        <img src="{path}" alt="Image Preview">
    </div>
</body>
</html>
"""

MARKDOWN_HTML = """
<html>
<head>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/github-markdown-css/github-markdown.min.css">
    <style>
        body {{
            margin: 0;
            padding: 20px;
            background-color: white;
        }}
        .markdown-body {{
            box-sizing: border-box;
            min-width: 200px;
            max-width: 980px;
            margin: 0 auto;
        }}
    </style>
</head>
<body>
    <div class="markdown-body">
        {content}
    </div>
</body>
</html>
"""


class PreviewWidget(widgets.Widget):
    """Widget that can display both PDFs and images using WebEngineView."""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.set_layout("vertical", margin=0)
        self.toolbar = widgets.ToolBar()
        self.box.add(self.toolbar)
        self.toolbar.add_action(
            _("Zoom In"), icon="mdi.magnify-plus-outline", callback=self.zoom_in
        )
        self.toolbar.add_action(
            _("Zoom Out"), icon="mdi.magnify-minus-outline", callback=self.zoom_out
        )
        self.toolbar.add_action(
            _("Reset Zoom"), icon="mdi.magnify", callback=self.reset_zoom
        )
        self.web_view = webenginewidgets.WebEngineView()
        self.web_view.get_settings()["plugins_enabled"] = True
        self.zoom_factor = 1.0
        self.web_view.set_zoom(self.zoom_factor)
        self.box.add(self.web_view)
        self.set_default_view()
        self.current_file = None

    def set_default_view(self):
        """Show default content when no file is selected."""
        self.web_view.set_html(DEFAULT_HTML)
        self.current_file = None

    def load_file(self, file_path: Path | str):
        """Load a file for preview."""
        if isinstance(file_path, str):
            file_path = Path(file_path)

        if not file_path.exists():
            logger.error("File does not exist: %s", file_path)
            self.set_default_view()
            return

        self.current_file = file_path
        suffix = file_path.suffix.lower()

        if suffix == ".pdf":
            self.load_pdf(file_path)
        elif suffix in (".jpg", ".jpeg", ".png", ".bmp", ".gif"):
            self.load_image(file_path)
        else:
            logger.warning("Unsupported file type: %s", suffix)
            self.set_default_view()

    def load_pdf(self, file_path: Path):
        """Load a PDF file into the web view."""
        logger.info("Loading PDF: %s", file_path)
        self.web_view.load_url(file_path.as_uri())

    def load_image(self, file_path: Path):
        """Load an image file into the web view with HTML wrapper."""
        logger.info("Loading image: %s", file_path)
        mime_type, _ = mimetypes.guess_type(str(file_path))
        if not mime_type:
            mime_type = "image/jpeg"  # Default fallback

        path = file_path.as_uri()
        content = IMAGE_HTML.format(path=path)
        url = core.Url.from_local_file(str(file_path.parent))
        self.web_view.setHtml(content, baseUrl=url)

    def load_markdown(self, content: str):
        """Load markdown content for preview."""
        logger.info("Loading markdown content")
        from mkconvert import ComrakParser

        parser = ComrakParser()
        html_content = parser.convert(content)
        html = MARKDOWN_HTML.format(content=html_content)
        self.web_view.setHtml(html)
        self.current_file = None  # Not associated with a file anymore

    def zoom_in(self):
        """Increase zoom level."""
        self.zoom_factor = min(3.0, self.zoom_factor + 0.25)
        self.web_view.set_zoom(self.zoom_factor)

    def zoom_out(self):
        """Decrease zoom level."""
        self.zoom_factor = max(0.25, self.zoom_factor - 0.25)
        self.web_view.set_zoom(self.zoom_factor)

    def reset_zoom(self):
        """Reset zoom to default level."""
        self.zoom_factor = 1.0
        self.web_view.set_zoom(self.zoom_factor)

        # If we're viewing a file, reload it to ensure proper display
        if self.current_file:
            self.load_file(self.current_file)
