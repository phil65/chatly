"""Top-level package for DataCook QtCharts Plugin."""

from prettyqt import webenginewidgets, widgets

from chatly.core.translate import _


class HelpPage(widgets.Widget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.set_title(_("Help"))
        self.set_icon("mdi.help")
        self.set_layout("horizontal", margin=0)
        webview = webenginewidgets.WebEngineView()
        webview.set_attributes(native_window=False)
        webview.load_url("https://google.com")
        webview.set_zoom(1.25)
        self.box.add(webview)


if __name__ == "__main__":
    app = widgets.app()
    w = HelpPage()
    w.show()
    app.main_loop()
