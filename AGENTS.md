# AGENTS.md

## Overview

Chatly is an early-stage Qt desktop app (PySide6 via [prettyqt](https://github.com/phil65/prettyqt))
for converting documents (PDF, images) to Markdown with the converter backends of
[docler](https://github.com/phil65/docler), and previewing the results. The Chat and
OCR/"Datasets" pages are still empty placeholders. There is no library API; the product is the GUI.

## Architecture

- `src/chatly/__main__.py`: entry point (`chatly` / `chatly-gui` scripts). Parses `-v`, creates
  `MainApp` and `MainWindow`, runs the Qt main loop.
- `src/chatly/application.py`: `MainApp(widgets.Application)`, app-wide signals.
- `src/chatly/windows/main_window.py`: `MainWindow(custom_widgets.SidebarWidget)`. Builds all
  pages, adds sidebar tabs (Start, Documents, Datasets, Chat), status bar, and connects to the
  thread pool signals.
- `src/chatly/pages/`: one widget per page. `start_page.py` is the core workflow: file tree, then
  preview, then converter buttons. A conversion runs on `threads.pool` and calls
  `anyenv.run_sync(converter.convert_file(path))`. The result goes into `DocumentManager`.
  `documents_page.py` lists converted documents with docked preview and raw-Markdown views.
  `settings_page.py` edits `core.config.config`. `browser_page.py` (HelpPage) and `log_page.py`
  are created but not added as tabs.
- `src/chatly/core/`:
  - `converters.py`: `CONVERTERS` dict `{NAME: converter class}` built from docler's
    provider classes (`docler.converters.*_provider`).
  - `document_manager.py`: `DocumentManager` singleton (`DocumentManager.instance()`), a
    QObject that stores `docler.models.Document`s and emits `document_added` / `document_removed`.
  - `threads.py`: `Worker` (QRunnable with signals) and the global `pool` (busy/job-count signals).
  - `config.py`: pydantic `Config` model with a module-level `config` instance (not persisted yet).
  - `constants.py`: platformdirs paths, frozen (PyInstaller) detection.
  - `translate.py`: gettext `_()` helper (no locales ship, so it falls back to identity).
- `src/chatly/widgets/preview_widget.py`: `PreviewWidget`, a WebEngine view for PDF/images, and
  Markdown rendered through `mkconvert.ComrakParser`. `widgets/vector_dbs/` holds empty stubs.
- `src/chatly/log.py`: `get_logger(name)` (template-provided).
- Packaging for Windows: `main.spec` (PyInstaller) and `install.nsi` (NSIS). These are used in
  the `release` job of `.github/workflows/build.yml`.

## Where to look

| Task | Location |
| --- | --- |
| Add or remove a document converter | `src/chatly/core/converters.py` |
| Conversion flow / threading | `src/chatly/pages/start_page.py`, `src/chatly/core/threads.py` |
| Stored documents | `src/chatly/core/document_manager.py`, `src/chatly/pages/documents_page.py` |
| Preview rendering | `src/chatly/widgets/preview_widget.py` |
| New sidebar page | `src/chatly/pages/` + export in `pages/__init__.py` + `add_tab` in `windows/main_window.py` |
| Settings | `src/chatly/core/config.py`, `src/chatly/pages/settings_page.py` |
| CI | `.github/workflows/build.yml`, `.github/workflows/documentation.yml` |
| Dev tasks | `duties.py` |

## Commands

```bash
uv sync --all-extras                 # setup (default groups: dev, lint, docs)
uv run chatly -v                     # run the app (needs a display)
uv run pytest                        # tests
uvx ruff check . && uvx ruff format --check .
uv run ty check                      # type check (src/ only, see [tool.ty.src])
uv run deptry src                    # dependency hygiene
uv run mkdocs-mknodes build          # docs (README + auto-generated API pages)
uv build
uv run duty lint | lint_check | test | build | serve | version
```

Headless smoke test of the GUI: `QT_QPA_PLATFORM=offscreen uv run python -c "..."` that builds
`MainApp()` and `MainWindow()`.

## Conventions

- Python >= 3.13, `from __future__ import annotations`, ruff (line length 100, preview format,
  Google docstrings).
- Use prettyqt's snake_case wrappers (`widgets.Label`, `set_layout`, `box.add`, `set_title`) and
  not raw Qt calls where a wrapper exists. Icons are qtawesome names (`"mdi.*"`).
- UI strings go through `_()` from `chatly.core.translate`.
- ty fails on warnings. Use targeted `# ty: ignore[rule]` only; mypy-style ignores are dead.
- Tests live in `tests/`. There is only a placeholder test right now; pytest-qt is available
  (`qtbot`) for widget tests.

## Pitfalls

- Copier-managed (template `copier-phil65`, see `.copier-answers.yml`): `pyproject.toml` tool
  sections, `.github/workflows/*`, `duties.py`, `mkdocs.yml`, `.pre-commit-config.yaml`,
  `src/chatly/log.py`. Don't hand-edit template-owned parts. Add dependencies below the
  `# Only add below (Copier)` markers. Update with
  `uvx --with copier-templates-extensions copier update --trust`.
- `comrak` is a direct dependency only for `mkconvert`'s ComrakParser (deptry DEP002 ignore).
  The `mkconvert[comrak]` extra skips comrak on Python 3.14.
- Most docler converters call external services and need API keys (Mistral, LlamaParse,
  Azure, Upstage, DataLab) or heavy local models (Docling, Marker). Don't trigger them in tests.
- Importing `chatly.core.constants` creates the user data, cache and log dirs (`ensure_exists=True`).
- `widgets.Application` must exist before you create any widget. GUI code needs a display or
  `QT_QPA_PLATFORM=offscreen`. CI installs Qt libs via `tlambert03/setup-qt-libs`.
- `uv.lock` is gitignored.
