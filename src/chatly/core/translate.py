from __future__ import annotations

# import ctypes
import gettext

from chatly.core.constants import LANG_DIR, MODULE_NAME


class LangProvider:
    lang = gettext.gettext

    @classmethod
    def set_language(cls, language):
        lang = gettext.translation(
            MODULE_NAME, localedir=str(LANG_DIR), languages=[language]
        )
        lang.install(None)
        cls.lang = lang.gettext


def _(text: str) -> str:
    return LangProvider.lang(text)
