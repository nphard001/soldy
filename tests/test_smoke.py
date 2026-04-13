"""Smoke tests for soldy."""

from __future__ import annotations

from click.testing import CliRunner

from soldy.cli import main


def test_version() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "0.1.0" in result.output


def test_log() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["log", "Alice", "Hello"])
    assert result.exit_code == 0
    assert "[Alice] Hello" in result.output
