#!/usr/bin/env python3
#
# SPDX-FileCopyrightText: Copyright (c) 2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Validate this workspace's manifest without the sibling checkouts.

CI has no siblings in `repos/`, and uv cannot resolve a workspace whose members
are absent -- `uv sync`, `uv lock` and `uv run` all fail with "references a
workspace in tool.uv.sources ... but is not a workspace member". That is not a
thing to work around: resolution genuinely needs the members. So CI checks what
it can see, which is whether the manifest agrees with itself.

The invariant that matters here: every dependency redirected to a local
checkout must be declared as a dependency, and every sibling dependency must be
redirected. A source without a requirement is dead configuration; a requirement
without a source resolves from PyPI while the workspace silently stops testing
the local branch, which is the whole point of this repo.
"""

from __future__ import annotations

from pathlib import Path
import re
import sys
import tomllib

MANIFEST = Path(__file__).resolve().parents[1] / "pyproject.toml"

#: Everything this workspace exists to wire together lives under this prefix or
#: is named explicitly; anything else in `dependencies` is an ordinary package.
SIBLING_PATTERN = re.compile(r"^(pyvider|provide-|flavor|plating|tofusoup|supsrc)")

REQUIREMENT_NAME = re.compile(r"^([A-Za-z0-9._-]+)")


def requirement_name(requirement: str) -> str:
    match = REQUIREMENT_NAME.match(requirement.strip())
    return match.group(1).lower().replace("_", "-") if match else ""


def main() -> int:
    problems: list[str] = []

    try:
        manifest = tomllib.loads(MANIFEST.read_text())
    except (OSError, tomllib.TOMLDecodeError) as exc:
        print(f"❌ {MANIFEST.name} does not parse: {exc}")
        return 1

    project = manifest.get("project", {})
    uv = manifest.get("tool", {}).get("uv", {})
    members = uv.get("workspace", {}).get("members")
    sources = uv.get("sources", {})

    if not members:
        problems.append("[tool.uv.workspace] declares no members")

    declared = {requirement_name(r): r for r in project.get("dependencies", [])}
    workspace_sources = {
        name.lower().replace("_", "-")
        for name, source in sources.items()
        if isinstance(source, dict) and source.get("workspace") is True
    }

    for name in sorted(workspace_sources - declared.keys()):
        problems.append(
            f"[tool.uv.sources] redirects {name!r} to a workspace member, "
            "but nothing depends on it"
        )

    for name in sorted(declared.keys() - workspace_sources):
        if SIBLING_PATTERN.match(name):
            problems.append(
                f"{name!r} is a sibling package but has no "
                "[tool.uv.sources] redirect, so it would resolve from PyPI"
            )

    if problems:
        print(f"❌ {len(problems)} problem(s) in {MANIFEST.name}:\n")
        for problem in problems:
            print(f"   • {problem}")
        return 1

    print(f"✅ {MANIFEST.name} is self-consistent")
    print(f"   members         : {', '.join(members)}")
    print(f"   dependencies    : {len(declared)}")
    print(f"   workspace-routed: {len(workspace_sources)}")
    print("\nResolution is not attempted: it requires the sibling checkouts,")
    print("which CI deliberately does not clone. That is a local-only check.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
