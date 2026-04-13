"""soldy CLI — the only interface."""

from __future__ import annotations

import click


@click.group()
@click.version_option()
def main() -> None:
    """Minimal append-only dialogue logger."""


@main.command()
@click.argument("name")
@click.argument("message")
def log(name: str, message: str) -> None:
    """Log what someone said."""
    # TODO: implement actual SOLD write
    click.echo(f"[{name}] {message}")
