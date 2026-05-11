#!/usr/bin/env python3
"""Open the Lantern local chat shell without starting servers or agents.

This launcher is intentionally small:
- resolves the checked-in static HTML shell;
- opens it with the operating system default browser;
- prints the file URL and boundary text;
- does not start Flask, tunnels, agents, sensors, or MCP tools.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
import webbrowser


REPO_ROOT = Path(__file__).resolve().parents[1]
CHAT_SHELL = REPO_ROOT / "apps" / "lantern-local-chat" / "index.html"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Open the Lantern local chat shell.")
    parser.add_argument(
        "--print-only",
        action="store_true",
        help="Print the local file URL without opening a browser.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not CHAT_SHELL.exists():
        print(f"Lantern local chat shell not found: {CHAT_SHELL}", file=sys.stderr)
        return 1

    url = CHAT_SHELL.resolve().as_uri()
    print("Lantern local chat shell")
    print(f"URL: {url}")
    print("Boundary: static local page only; no command execution, no agents, no tunnels, no public writes.")

    if not args.print_only:
        webbrowser.open(url)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
