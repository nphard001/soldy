"""Smoke tests for soldy."""

from __future__ import annotations

import pytest
from click.testing import CliRunner

from soldy.cli import main


@pytest.fixture()
def runner() -> CliRunner:
    return CliRunner()




@pytest.mark.parametrize("cmd", ["init", "text", "list"])
def test_commands_exist(runner: CliRunner, cmd: str) -> None:
    result = runner.invoke(main, [cmd, "--help"])
    assert result.exit_code == 0
