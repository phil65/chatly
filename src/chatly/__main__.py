"""Entry point for Chatly application."""

from __future__ import annotations

import argparse
import logging
import sys

from chatly.application import MainApp
from chatly.windows.main_window import MainWindow


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Chatly - Agent desktop app")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose logging"
    )
    return parser.parse_args()


def main() -> int:
    """Run the application."""
    args = parse_args()

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level)

    app = MainApp()
    window = MainWindow()
    window.show()
    return app.main_loop()


if __name__ == "__main__":
    sys.exit(main())
