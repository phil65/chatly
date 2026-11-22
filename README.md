# Chatly

[![PyPI License](https://img.shields.io/pypi/l/chatly.svg)](https://pypi.org/project/chatly/)
[![Package status](https://img.shields.io/pypi/status/chatly.svg)](https://pypi.org/project/chatly/)
[![Monthly downloads](https://img.shields.io/pypi/dm/chatly.svg)](https://pypi.org/project/chatly/)
[![Distribution format](https://img.shields.io/pypi/format/chatly.svg)](https://pypi.org/project/chatly/)
[![Wheel availability](https://img.shields.io/pypi/wheel/chatly.svg)](https://pypi.org/project/chatly/)
[![Python version](https://img.shields.io/pypi/pyversions/chatly.svg)](https://pypi.org/project/chatly/)
[![Implementation](https://img.shields.io/pypi/implementation/chatly.svg)](https://pypi.org/project/chatly/)
[![Releases](https://img.shields.io/github/downloads/phil65/chatly/total.svg)](https://github.com/phil65/chatly/releases)
[![Github Contributors](https://img.shields.io/github/contributors/phil65/chatly)](https://github.com/phil65/chatly/graphs/contributors)
[![Github Discussions](https://img.shields.io/github/discussions/phil65/chatly)](https://github.com/phil65/chatly/discussions)
[![Github Forks](https://img.shields.io/github/forks/phil65/chatly)](https://github.com/phil65/chatly/forks)
[![Github Issues](https://img.shields.io/github/issues/phil65/chatly)](https://github.com/phil65/chatly/issues)
[![Github Issues](https://img.shields.io/github/issues-pr/phil65/chatly)](https://github.com/phil65/chatly/pulls)
[![Github Watchers](https://img.shields.io/github/watchers/phil65/chatly)](https://github.com/phil65/chatly/watchers)
[![Github Stars](https://img.shields.io/github/stars/phil65/chatly)](https://github.com/phil65/chatly/stars)
[![Github Repository size](https://img.shields.io/github/repo-size/phil65/chatly)](https://github.com/phil65/chatly)
[![Github last commit](https://img.shields.io/github/last-commit/phil65/chatly)](https://github.com/phil65/chatly/commits)
[![Github release date](https://img.shields.io/github/release-date/phil65/chatly)](https://github.com/phil65/chatly/releases)
[![Github language count](https://img.shields.io/github/languages/count/phil65/chatly)](https://github.com/phil65/chatly)
[![Github commits this month](https://img.shields.io/github/commit-activity/m/phil65/chatly)](https://github.com/phil65/chatly)
[![Package status](https://codecov.io/gh/phil65/chatly/branch/main/graph/badge.svg)](https://codecov.io/gh/phil65/chatly/)

[Read the documentation!](https://phil65.github.io/chatly/)

Chatly is a Qt desktop app for turning documents into Markdown. You browse your files, preview
PDFs and images, and convert them with one click using any of the document converters from
[docler](https://github.com/phil65/docler). The converted documents stay available for review in
the app.

> **Status:** early development. Document conversion and preview work. The Chat and
> Datasets pages are placeholders for now.

## Installation

```bash
pip install chatly
# or
uv tool install chatly
```

Requires Python 3.13+. The GUI is built on [prettyqt](https://github.com/phil65/prettyqt) /
PySide6 (with Qt WebEngine for previews).

## Quickstart

```bash
chatly          # start the app
chatly -v       # start with debug logging
```

1. On the **Start** page, select a PDF or image in the file tree on the left. A preview opens
   in the middle.
2. Click a converter on the right (`datalab`, `docling`, `marker`, `mistral`, `llamaparse`,
   `azure` or `upstage`). The conversion runs in the background.
3. Open the **Documents** page to see the converted documents, a rendered Markdown preview and
   the raw Markdown.

Most converters are cloud services and read their API keys from the environment
(for example `MISTRAL_API_KEY`, `LLAMAPARSE_API_KEY`, `DATALAB_API_KEY`, `UPSTAGE_API_KEY`, and
`AZURE_DOC_INTELLIGENCE_ENDPOINT` / `AZURE_DOC_INTELLIGENCE_KEY`). `docling` and `marker` run locally but download models on first use. See the
[docler documentation](https://phil65.github.io/docler/) for the details of each provider.

## Features

- File browser for PDF and image files, with an embedded preview (Qt WebEngine)
- Seven document-to-Markdown backends through docler, run on a background thread pool
- Document list with a rendered preview (comrak) and the raw Markdown side by side
- Settings dialog for theme, style, toolbar style and logging (work in progress: values are
  not applied or saved yet)
- Window and dock layout is saved between sessions

## Development

```bash
git clone https://github.com/phil65/chatly
cd chatly
uv sync --all-extras
uv run chatly
uv run pytest
```

## License

MIT
