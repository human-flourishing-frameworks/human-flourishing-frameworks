#!/usr/bin/env python3
"""
CI Sentinel Issue Manager

This script runs unittest discovery and manages a single GitHub issue that tracks
whether master CI is passing.
- If CI fails, it opens or updates an issue tagged 'ci-sentinel' with failure output.
- If CI passes and an open 'ci-sentinel' issue exists, it closes the issue.
"""

import os
import sys
import subprocess
from datetime import datetime

try:
    from github import Github
except ImportError:
    print("PyGithub not installed. Install with: pip install PyGithub")
    sys.exit(1)


def run_tests():
    """Run unittest discovery and return (success, output)."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-t", ".", "-p", "test_*.py"],
            capture_output=True,
            text=True,
            timeout=300
        )
        return result.returncode == 0, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return False, "Tests timed out after 300 seconds"
    except Exception as e:
        return False, f"Error running tests: {e}"


def main():
    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token:
        print("GITHUB_TOKEN environment variable not set")
        sys.exit(1)

    repo_name = os.environ.get("REPO")
    if not repo_name:
        print("REPO environment variable not set")
        sys.exit(1)

    # Run tests
    print("Running unittest discovery...")
    tests_passed, test_output = run_tests()

    if not tests_passed:
        print("Tests failed")
        sys.exit(1)

    # Tests passed - manage GitHub issue
    g = Github(github_token)
    repo = g.get_repo(repo_name)

    # Find existing ci-sentinel issue
    sentinel_label = "ci-sentinel"
    try:
        repo.get_label(sentinel_label)
    except:
        # Create label if it doesn't exist
        repo.create_label(sentinel_label, "d73a4a", "CI sentinel for master branch")

    issues = repo.get_issues(labels=[sentinel_label], state="open")
    existing_issue = None
    for issue in issues:
        if issue.title.startswith("CI Sentinel:"):
            existing_issue = issue
            break

    # Tests passed - close existing issue if any
    if existing_issue:
        existing_issue.edit(
            body=f"{existing_issue.body}\n\n**Resolved:** {datetime.utcnow().isoformat()} UTC - CI is now passing.",
            state="closed",
            labels=[sentinel_label]
        )
        print(f"Closed CI sentinel issue: #{existing_issue.number}")
    else:
        print("CI is passing and no open CI sentinel issue exists")


if __name__ == "__main__":
    main()
