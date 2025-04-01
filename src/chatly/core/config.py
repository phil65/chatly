"""Config."""

from __future__ import annotations

import logging

from pydantic import BaseModel, Field


class Config(BaseModel):
    app_theme: str = Field(default="dark")
    style: str = Field(default="default")
    code_viewer: str = Field(default="default")
    toolbar_style: str = Field(default="icon")
    language: str = Field(default="en")
    log_level: int = Field(default=logging.INFO)
    log_format: str = Field(default="%(asctime)s - %(levelname)s - %(message)s")
    app_style: str = Field(default="Fusion")
    show_context_shortcuts: bool = Field(default=False)


config = Config()
