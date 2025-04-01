from __future__ import annotations

# import ctypes
import logging
import pathlib
import sys

import platformdirs

import chatly


logger = logging.getLogger(__name__)

MODULE_NAME = chatly.__name__

dirs = platformdirs.AppDirs(
    chatly.__title__, appauthor=False, roaming=True, ensure_exists=True
)

if getattr(sys, "frozen", False):
    # pylint: disable=no-member,protected-access
    APP_DIR = pathlib.Path(sys._MEIPASS)  # type: ignore
    FROZEN = True
else:
    APP_DIR = pathlib.Path(__file__).parent.parent.parent  # importlib.resources.files?
    FROZEN = False

CACHE_DIR = pathlib.Path(dirs.user_cache_dir)
DATA_DIR = pathlib.Path(dirs.user_data_dir)
LOG_DIR = pathlib.Path(dirs.user_log_dir)
MODULE_PATH = APP_DIR / MODULE_NAME
RESOURCES_DIR = MODULE_PATH / "resources"
FONTS_DIR = RESOURCES_DIR / "fonts"
LANG_DIR = MODULE_PATH / "locales"
PLUGINS_DIR = MODULE_PATH / "plugins"
PLUGINS_EXT = "plugin"

DEFAULT_SETTINGS_PATH = MODULE_PATH / "config_default.yaml"
USER_SETTINGS_PATH = DATA_DIR / "config.yaml"

LOG_CONFIG_FILE = MODULE_PATH / "logging.yaml"
HELP_INDEX_HTML = MODULE_PATH / "docs" / "index.html"
LOG_PATH = LOG_DIR / "log.txt"

LOGO_SPLASH = RESOURCES_DIR / "logo.jpg"
LOGO_ICON = RESOURCES_DIR / "icon.ico"
