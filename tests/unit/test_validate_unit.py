#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Unit tests for validate.sh script with mocked subprocess calls."""

from __future__ import annotations

from pathlib import Path

import pytest
from provide.testkit import (
    ScriptExecutionContext,
    assert_script_failure,
)


@pytest.fixture
def validate_script(scripts_dir: Path) -> Path:
    """Return path to validate.sh script.

    Args:
        scripts_dir: Path to scripts directory.

    Returns:
        Path to validate.sh.
    """
    return scripts_dir / "validate.sh"


def test_validate_help_flag(
    script_execution_context: ScriptExecutionContext,
    validate_script: Path,
) -> None:
    """Test validate.sh with --help flag."""
    result = script_execution_context.run_script(validate_script, args=["--help"])

    # Script may return 0 or 1 depending on implementation
    assert "Usage:" in result.stdout or "help" in result.stdout.lower()


def test_validate_requires_git(
    script_execution_context: ScriptExecutionContext,
    validate_script: Path,
) -> None:
    """Test validate.sh detects missing git."""
    env = script_execution_context.env.copy() if script_execution_context.env else {}
    env["PATH"] = "/nonexistent"
    script_execution_context.env = env

    result = script_execution_context.run_script(validate_script)

    assert_script_failure(result)
    assert "git" in result.stdout.lower() or "git" in result.stderr.lower()


def test_validate_checks_python_version(
    script_execution_context: ScriptExecutionContext,
    validate_script: Path,
) -> None:
    """Test validate.sh checks Python version."""
    result = script_execution_context.run_script(validate_script)

    # Will fail due to missing prerequisites but should check Python
    assert "python" in result.stdout.lower() or "python" in result.stderr.lower()
