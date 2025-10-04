from __future__ import annotations

import logging

from prettyqt import core, custom_widgets, widgets

from chatly.core.config import config
from chatly.core.translate import _


TOOLBAR_STYLES = dict(
    icon=_("Icon"),
    text=_("Text"),
    text_beside_icon=_("Text beside icon"),
    text_below_icon=_("Text below icon"),
)

LOG_LEVELS = {
    logging.DEBUG: _("Debug"),
    logging.INFO: _("Info"),
    logging.WARNING: _("Warning"),
    logging.CRITICAL: _("Critical"),
    logging.ERROR: _("Error"),
}


class GeneralSettings(widgets.Widget):
    settings_updated = core.Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setMaximumWidth(1000)
        self.set_title(_("General settings"))
        self.set_icon("mdi.application")
        self.set_layout("form")
        self.box.set_size_constraint("minimum")
        self.cb_apptheme = widgets.ComboBox()
        self.cb_style = widgets.ComboBox()
        self.cb_toolbar_style = widgets.ComboBox()
        # self.cb_language = widgets.ComboBox()
        self.combo_log_level = widgets.ComboBox()
        self.lineedit_log_format = widgets.LineEdit()

        show_shortcuts = config.show_context_shortcuts
        self.chk_context_shortcuts = widgets.CheckBox(
            _("Show context menu shortcuts"), checked=show_shortcuts
        )

        self.box += widgets.Label(_("Appearance settings")).set_bold()
        self.box += (widgets.Label(_("App theme")), self.cb_apptheme)
        self.box += (widgets.Label(_("App style")), self.cb_style)
        self.box += (widgets.Label(_("Toolbar style")), self.cb_toolbar_style)
        self.box += widgets.Label(_("Log settings")).set_bold()
        self.box += (widgets.Label(_("Log level")), self.combo_log_level)
        self.box += (widgets.Label(_("Log format")), self.lineedit_log_format)
        self.box += widgets.Label(_("Misc")).set_bold()
        # self.box += (widgets.Label(_("Language")), self.cb_language)
        self.box += ("", self.chk_context_shortcuts)
        self.cb_toolbar_style.add_items(TOOLBAR_STYLES)
        self.cb_toolbar_style.set_value(config.toolbar_style)
        self.combo_log_level.add_items(LOG_LEVELS)
        self.combo_log_level.set_value(config.log_level)
        self.lineedit_log_format.set_value(config.log_format)
        self.cb_apptheme.add_items(widgets.Application.get_available_themes())
        self.cb_apptheme.set_value(config.app_theme)
        self.cb_style.add_items(widgets.StyleFactory.keys())
        self.cb_style.set_text(config.app_style)

        # self.cb_language.add_items(appmanager.instance.languages)
        # self.cb_language.set_value(config.language)

    def accept(self):
        config.app_theme = self.cb_apptheme.get_value()
        config.app_style = self.cb_style.text()
        config.toolbar_style = self.cb_toolbar_style.get_value()
        # config.language = self.cb_language.get_value()
        config.log_format = self.lineedit_log_format.text()
        config.log_level = self.combo_log_level.get_value()
        config.show_context_shortcuts = self.chk_context_shortcuts.get_value()
        self.settings_updated.emit()


class SettingsPage(custom_widgets.SidebarWidget):
    BUTTON_WIDTH = 250

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.set_title(_("Settings"))
        self.set_icon("mdi.wrench-outline")
        self.resize(1000, 600)
        self.general_settings = GeneralSettings()
        self.sidebar.set_style("text_beside_icon")
        self.add_tab(self.general_settings, _("General"), icon="mdi.application")
        button_box = widgets.DialogButtonBox.create(save=self.accept, cancel=self.close)
        button_box.setContentsMargins(0, 0, 20, 20)
        self.main_layout += button_box

    def accept(self):
        self.general_settings.accept()
        self.close()


if __name__ == "__main__":
    app = widgets.app()
    w = SettingsPage()
    w.show()
    app.main_loop()
