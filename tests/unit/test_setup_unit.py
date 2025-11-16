#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Unit tests for setup.sh script with mocked subprocess calls."""

from __future__ import annotations

from pathlib import Path

import pytest
from provide.testkit import (
    ScriptExecutionContext,
    assert_script_failure,
)


@pytest.fixture
def setup_script(scripts_dir: Path) -> Path:
    """Return path to setup.sh script.

    Args:
        scripts_dir: Path to scripts directory.

    Returns:
        Path to setup.sh.
    """
    return scripts_dir / "setup.sh"


def test_setup_requires_python(
    script_execution_context: ScriptExecutionContext,
    setup_script: Path,
) -> None:
    """Test setup.sh fails when Python is not available."""
    env = script_execution_context.env.copy() if script_execution_context.env else {}
    env["PATH"] = "/nonexistent"
    script_execution_context.env = env

    result = script_execution_context.run_script(setup_script)

    assert_script_failure(result)
    assert "python" in result.stderr.lower() or "python" in result.stdout.lower()


def test_setup_detects_python_version(
    script_execution_context: ScriptExecutionContext,
    setup_script: Path,
) -> None:
    """Test setup.sh detects Python version."""
    # This will fail because we don't have all prerequisites, but we can check version detection
    result = script_execution_context.run_script(setup_script)

    # Check that it attempts to detect Python version
    assert "python" in result.stdout.lower() or "python" in result.stderr.lower()
