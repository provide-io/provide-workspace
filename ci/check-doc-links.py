#!/usr/bin/env python3
#
# SPDX-FileCopyrightText: Copyright (c) 2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Check that the links in this repo's markdown go somewhere.

A link checker filed provide-io/provide-workspace#1 in March, the workflow that
ran it was removed, and its logs have since expired -- so the report outlived
both the evidence for it and anything that could re-test it. Nothing has
checked a link here since. This is that check, in the repo, where it is
re-runnable.

Two kinds of link, held to two different standards, because they fail for
different reasons:

A **relative link** is this repo's own claim about its own layout, so a target
that is not there is always a defect and always fails the check. Where such a
link carries a ``#fragment`` and points at markdown, the heading is checked too:
a link into a section that was renamed is broken in the way that matters to a
reader, while still resolving as a file.

An **external link** can fail without anyone here having done anything wrong --
a rate limit, a timeout, a site that is down for the afternoon. Only a
definitive answer from the server counts: 404 and 410, meaning the resource is
gone. Anything else is reported and tolerated, so a flaky network cannot fail
this repo's CI and teach everyone to ignore it.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import subprocess  # nosec B404 - git ls-files, no shell, fixed argv
import sys
import urllib.error
import urllib.request

REPO_ROOT = Path(__file__).resolve().parents[1]

#: Inline markdown links: the target is everything up to the closing paren.
#: Reference-style definitions are matched separately below.
INLINE_LINK = re.compile(r"\[[^\]]*\]\(\s*(<[^>]+>|[^)\s]+)")

#: Reference definitions, e.g. ``[label]: https://example.com``.
REFERENCE_LINK = re.compile(r"^\[[^\]]+\]:\s*(\S+)", re.MULTILINE)

#: ATX headings, whose text becomes the anchor a ``#fragment`` addresses.
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*#*$", re.MULTILINE)

#: Anything a fragment cannot be resolved against by reading the file.
NON_HTTP_SCHEME = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")

DEFINITELY_GONE = (404, 410)

TIMEOUT_SECONDS = 20


def tracked_markdown() -> list[Path]:
    """Markdown files git knows about, which excludes .venv and vendored trees."""
    listed = subprocess.run(  # nosec B603 - fixed argv, no shell
        ["git", "ls-files", "*.md"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return [REPO_ROOT / name for name in listed.stdout.split()]


def anchor_slug(heading: str) -> str:
    """Slugify *heading* the way GitHub does: fold case, drop punctuation, join on -."""
    text = re.sub(r"[^\w\s-]", "", heading.strip().lower())
    return re.sub(r"[\s]+", "-", text)


def anchors_in(path: Path) -> set[str]:
    return {anchor_slug(heading) for heading in HEADING.findall(path.read_text(encoding="utf-8"))}


def targets_in(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    found = INLINE_LINK.findall(text) + REFERENCE_LINK.findall(text)
    return [target.strip("<>") for target in found]


def check_relative(source: Path, target: str) -> str | None:
    """Return a problem describing *target*, or None where it resolves."""
    path_part, _, fragment = target.partition("#")
    if not path_part:
        # A bare "#section" addresses the file it sits in.
        return None if not fragment or anchor_slug(fragment) in anchors_in(source) else f"no heading '#{fragment}'"

    resolved = (source.parent / path_part).resolve()
    if not resolved.exists():
        return "no such file"
    if fragment and resolved.suffix == ".md" and anchor_slug(fragment) not in anchors_in(resolved):
        return f"no heading '#{fragment}' in {path_part}"
    return None


def check_external(url: str) -> tuple[str | None, str | None]:
    """Return (problem, tolerated) for *url* -- at most one of them is set."""
    request = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "provide-workspace-link-check"})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:  # nosec B310 - http(s) only, checked below
            return None, None if response.status < 400 else f"HTTP {response.status}"
    except urllib.error.HTTPError as error:
        if error.code in DEFINITELY_GONE:
            return f"HTTP {error.code}", None
        return None, f"HTTP {error.code}"
    except Exception as error:  # noqa: BLE001 - any transport failure is tolerated alike
        return None, type(error).__name__


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skip-external",
        action="store_true",
        help="Check only relative links, leaving the network alone.",
    )
    args = parser.parse_args()

    files = tracked_markdown()
    problems: list[str] = []
    tolerated: list[str] = []
    relative_count = 0
    external_count = 0

    for source in files:
        for target in targets_in(source):
            name = source.relative_to(REPO_ROOT)
            if target.startswith(("http://", "https://")):
                external_count += 1
                if args.skip_external:
                    continue
                problem, excused = check_external(target)
                if problem:
                    problems.append(f"{name} -> {target} ({problem})")
                elif excused:
                    tolerated.append(f"{name} -> {target} ({excused})")
            elif NON_HTTP_SCHEME.match(target):
                # mailto:, tel: and friends address nothing this can open.
                continue
            else:
                relative_count += 1
                problem = check_relative(source, target)
                if problem:
                    problems.append(f"{name} -> {target} ({problem})")

    for excused in tolerated:
        print(f"   ~ unreachable, not counted against this repo: {excused}")

    if problems:
        print(f"❌ {len(problems)} broken link(s):\n")
        for problem in problems:
            print(f"   • {problem}")
        return 1

    checked_external = 0 if args.skip_external else external_count
    print(f"✅ links resolve in {len(files)} markdown file(s)")
    print(f"   relative: {relative_count}")
    print(f"   external: {checked_external} checked, {len(tolerated)} unreachable and tolerated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
