#!/usr/bin/env python3
"""Check a repo against the foundry user hardening baseline."""

from __future__ import annotations

import argparse
import fnmatch
import json
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = REPO_ROOT / "policies" / "foundry-user-repo-hardening.v1.json"


def load_policy(policy_path: Path = POLICY_PATH) -> dict:
    return json.loads(policy_path.read_text(encoding="utf-8"))


def tracked_like_files(repo_root: Path) -> list[Path]:
    skipped = {".git", ".venv", "__pycache__", "dist", ".claude"}

    def is_skipped(path: Path) -> bool:
        rel_parts = path.relative_to(repo_root).parts
        return any(part in skipped for part in rel_parts)

    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), "ls-files"],
            check=True,
            capture_output=True,
            text=True,
        )
        files: list[Path] = []
        for rel in result.stdout.splitlines():
            rel = rel.strip()
            if not rel:
                continue
            path = repo_root / rel
            if path.is_file() and not is_skipped(path):
                files.append(path)
        return files
    except Exception:
        # Fallback for non-git contexts: preserve prior behavior.
        pass

    files: list[Path] = []
    for path in repo_root.rglob("*"):
        if not path.is_file():
            continue
        if is_skipped(path):
            continue
        files.append(path)
    return files


def check_repo(repo_root: Path, policy: dict) -> list[str]:
    errors: list[str] = []

    for relative in policy["required_files"]:
        if not (repo_root / relative).is_file():
            errors.append(f"missing required file: {relative}")

    files = tracked_like_files(repo_root)
    markdown_files = [path.relative_to(repo_root).as_posix() for path in files if path.suffix.lower() == ".md"]
    for pattern in policy["forbidden_agent_behavior_markdown_patterns"]:
        for relative in markdown_files:
            if fnmatch.fnmatch(Path(relative).name.lower(), pattern.lower()) or fnmatch.fnmatch(relative.lower(), pattern.lower()):
                errors.append(f"forbidden behavior-shaping markdown: {relative}")

    allowed_runtime_files = set(policy.get("allowed_runtime_pattern_files", []))
    runtime_patterns = [item.lower() for item in policy["forbidden_runtime_patterns"]]
    retired_terms = [
        "lan" + "tern",
        "key" + "stone",
        "tar" + "dis",
        "cosmic-" + "door",
        "return " + "door",
        "dream" + "er",
    ]
    for path in files:
        relative = path.relative_to(repo_root).as_posix()
        if relative in allowed_runtime_files:
            continue
        if path.suffix.lower() not in {".py", ".js", ".ts", ".html", ".ps1", ".cmd", ".bat", ".md", ".json"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        if relative not in {"tools/check_foundry_repo_hardening.py"}:
            for term in retired_terms:
                if term in text:
                    errors.append(f"retired symbolic term '{term}': {relative}")
        for pattern in runtime_patterns:
            if pattern.lower() in text:
                errors.append(f"forbidden runtime doctrine hook '{pattern}': {relative}")

    return sorted(set(errors))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=REPO_ROOT)
    args = parser.parse_args()
    errors = check_repo(args.repo.resolve(), load_policy())
    if errors:
        for error in errors:
            print(error)
        return 1
    print("foundry repo hardening: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
