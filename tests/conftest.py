#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Shared pytest fixtures for provide-workenv tests."""

from __future__ import annotations

from pathlib import Path

# Ensure provide.testkit is imported early for setproctitle blocker
import provide.testkit  # noqa: F401
import pytest

# Import script testing utilities
from provide.testkit import (
    ScriptExecutionContext,
    bash_script_runner,
    isolated_workspace,
)

# Make utilities available to all tests
__all__ = [
    "ScriptExecutionContext",
    "bash_script_runner",
    "isolated_workspace",
    "scripts_dir",
]


@pytest.fixture
def scripts_dir() -> Path:
    """Return the path to the scripts directory.

    Returns:
        Path to provide-workenv/scripts directory.
    """
    return Path(__file__).parent.parent / "scripts"
