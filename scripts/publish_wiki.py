#!/usr/bin/env python3
"""Publish versioned wiki pages to the GitHub Wiki git remote."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WIKI_SOURCE = ROOT / "wiki"
WIKI_REMOTE = "https://github.com/The-Geek-Freaks/delta-kosmologie.wiki.git"
WIKI_URL = "https://github.com/The-Geek-Freaks/delta-kosmologie/wiki"


def run(args: list[str], cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    if args and args[0] == "git":
        args = [
            "git",
            "-c",
            "credential.helper=",
            "-c",
            "core.askPass=",
            "-c",
            "credential.interactive=false",
            *args[1:],
        ]
    env = {
        **os.environ,
        "GCM_INTERACTIVE": "Never",
        "GIT_TERMINAL_PROMPT": "0",
    }
    try:
        return subprocess.run(
            args,
            cwd=cwd,
            check=check,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=env,
            timeout=15,
        )
    except subprocess.TimeoutExpired as exc:
        output = exc.stdout if isinstance(exc.stdout, str) else ""
        return subprocess.CompletedProcess(args, 124, output + "\nCommand timed out.\n")


def copy_pages(target: Path) -> None:
    for page in WIKI_SOURCE.glob("*.md"):
        shutil.copy2(page, target / page.name)


def main() -> int:
    if not WIKI_SOURCE.exists():
        print("Missing wiki/ source directory.", file=sys.stderr)
        return 1

    with tempfile.TemporaryDirectory(prefix="delta-wiki-") as tmp:
        wiki_checkout = Path(tmp) / "wiki"
        remote = run(["git", "ls-remote", WIKI_REMOTE], check=False)
        if remote.returncode != 0:
            if remote.stdout:
                print(remote.stdout, file=sys.stderr)
            print(
                "\nGitHub has wiki enabled, but the backing .wiki.git remote is not initialized yet.\n"
                f"Open {WIKI_URL}, click 'Create the first page', save any Home page once,\n"
                "then rerun: python scripts/publish_wiki.py",
                file=sys.stderr,
            )
            return 2

        clone = run(["git", "clone", WIKI_REMOTE, str(wiki_checkout)])
        copy_pages(wiki_checkout)
        run(["git", "add", "."], cwd=wiki_checkout)
        status = run(["git", "status", "--porcelain"], cwd=wiki_checkout).stdout.strip()
        if not status:
            print("Wiki already up to date.")
            return 0

        author_name = os.environ.get("GIT_AUTHOR_NAME", "The-Geek-Freaks")
        author_email = os.environ.get("GIT_AUTHOR_EMAIL", "actions@users.noreply.github.com")
        run(["git", "config", "user.name", author_name], cwd=wiki_checkout)
        run(["git", "config", "user.email", author_email], cwd=wiki_checkout)
        run(["git", "commit", "-m", "Sync Delta Cosmology wiki"], cwd=wiki_checkout)
        push = run(["git", "push"], cwd=wiki_checkout, check=False)
        print(push.stdout)
        return push.returncode


if __name__ == "__main__":
    raise SystemExit(main())
