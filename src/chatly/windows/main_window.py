from __future__ import annotations

import logging

from prettyqt import custom_widgets, gui, widgets

import chatly
from chatly import application, pages
from chatly.core import threads
from chatly.core.translate import _


logger = logging.getLogger(__name__)


class MainWindow(custom_widgets.SidebarWidget):
    """Main window."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, show_settings=True, **kwargs)

        self.set_title(chatly.__title__)
        self.set_object_name("MainWindow")

        self.start_view = pages.StartPage()
        self.ocr_view = pages.OcrPage()
        self.chat_page = pages.ChatPage()
        self.help_page = pages.HelpPage()
        self.documents_page = pages.DocumentsPage()
        # self.explorer_page = pages.FileExplorerPage()
        self.log_page = pages.LogPage()

        self.add_tab(self.start_view, _("Start"), icon="mdi.google-nearby", shortcut="F1")
        self.add_tab(
            self.documents_page,
            _("Documents"),
            icon="mdi.file-document-outline",
            shortcut="F2",
        )

        self.add_tab(self.ocr_view, _("Datasets"), icon="mdi.database", shortcut="F3")
        self.add_tab(self.chat_page, _("Chat"), icon="mdi.chat", shortcut="F4")
        self.settings_menu.add_action(
            text=_("Settings"), icon="mdi.wrench-outline", callback=self.show_settings
        )
        self.statusbar = widgets.StatusBar()
        self.status_label = widgets.Label()
        self.statusbar.add_widget(self.status_label, permanent=True)
        self.update_statusbar(num_jobs=0)
        # self.statusbar.setup_default_bar()
        threads.pool.job_num_updated.connect(self.update_statusbar)
        threads.pool.exception_occured.connect(widgets.MessageBox.show_exception)

        # threads.pool.busy_on.connect(self.statusbar.progress_bar.show)
        # threads.pool.busy_off.connect(self.statusbar.progress_bar.hide)

        self.setStatusBar(self.statusbar)

        self.popup = custom_widgets.PopupInfo(parent=self)
        self.progress_dlg = widgets.ProgressDialog(parent=self)
        threads.pool.busy_blocking_on.connect(self.progress_dlg.show_message)
        threads.pool.busy_blocking_off.connect(self.progress_dlg.cancel)
        self.act_fullscreen = self.add_action(
            text=_("Fullscreen"),
            icon="mdi.fullscreen",
            callback=self.toggle_fullscreen,
            checkable=True,
            shortcut="F11",
            area="bottom",
        )
        widgets.app().settings_updated.emit()

    def show(self, *args, **kwargs):
        self.load_window_state(recursive=True)
        super().show(*args, **kwargs)
        self.act_fullscreen.setChecked(self.isFullScreen())

    def closeEvent(self, event):  # noqa: N802
        """override, gets executed when app gets closed."""
        self.save_window_state(recursive=True)
        super().closeEvent(event)
        widgets.app().closeAllWindows()
        event.accept()

    def keyPressEvent(self, event):  # noqa: N802
        """Keypress event override."""
        key_str = gui.KeySequence.to_shortcut_str(event.keyCombination())
        if key_str == "F11":
            self.toggle_fullscreen()
            event.accept()
            return None
        return super().keyPressEvent(event)

    def show_settings(self):
        settings_view = pages.SettingsPage()
        settings_view.show_blocking()

    def update_statusbar(self, num_jobs: int):
        if num_jobs > 0:
            text = f"{_('Running jobs')}: {num_jobs}"
        else:
            text = _("No running jobs")
        self.status_label.set_text(text)


if __name__ == "__main__":
    from chatly import application

    my_app = application.MainApp()
    mw = MainWindow()
    mw.show()
    my_app.main_loop()
