"""
The simple interface.
soldy init
soldy text
soldy list
"""

from __future__ import annotations

import os
import json
import click
from pathlib import Path
from soldy.path import WayMage
from soldy.model import SoldText, NTMage

def _out(obj) -> None:
    click.echo(json.dumps(obj, ensure_ascii=False))

def _rogue(pth: str | Path, content: str):
    p = Path(pth)
    p.parent.mkdir(parents=True, exist_ok=True)
    return p.write_text(content, encoding="utf-8")

@click.group()
@click.version_option()
def main() -> None:
    """A basic interface that implements simple SOLD-object"""

def cmd_init_rogue() -> None:
    pth = Path(WayMage.get_main_json())
    if not pth.is_file():
        pth.parent.mkdir(parents=True, exist_ok=True)
    
    pth_soldapi = pth.parent
    _rogue(pth, json.dumps({
        'cache': str(pth_soldapi / '_cache'),
        'agent': str(pth_soldapi / 'agent' / 'index.json')
    }, indent=1, ensure_ascii=False))
    
    return _out({"status": "initialized", "main_json": str(pth)})


    

@main.command("init")
@click.argument("name", required=False, default=None)
def cmd_init(name: str | None) -> None:
    """Initialize store, or register NAME."""
    if name is None:
        return cmd_init_rogue()
    
    pth = Path(WayMage.solve(f'{name}'))
    if not pth.is_file():
        pth.parent.mkdir(parents=True, exist_ok=True)

    pth_soldroot = pth.parent
    pth_raw = pth_soldroot / 'raw'
    pth_raw.mkdir(parents=True, exist_ok=True)

    _rogue(pth, json.dumps({
        'name': name,
        'schema': 'simple',
        'directories': [
            str(pth_raw)
        ]
    }, indent=1, ensure_ascii=False))
    return _out({"status": "initialized", "name": name, "index_json": str(pth), "raw_dir": str(pth_raw)})


@main.command("text")
@click.argument("name")
@click.argument("text")
def cmd_text(name: str, text: str) -> None:
    """Append a text entry for NAME."""
    dname0 = WayMage.solve(f'{name}.directories')[0]
    if not isinstance(dname0, str):
        raise ValueError(f"Expected a list of directories for '{name}.directories', got: {dname0!r}")
    pth = Path(dname0)

    sold_text = SoldText(name=name, text=text)
    sold_text.save(pth)
    return _out({"status": "text entry added", "addr": sold_text.addr})

@main.command("list")
@click.argument("name")
def cmd_list(name: str):
    """List all entries for NAME."""
    results = []
    dnames: list[str] = WayMage.solve(f"{name}.directories")
    if not isinstance(dnames, list):
        raise ValueError(f"Expected a list of directories for '{name}.directories', got: {dnames!r}")
    for dname in dnames:
        # collect *.json quickly by os.scandir
        if not os.path.isdir(dname):
            raise ValueError(f"Directory '{dname!r}' does not exist or is not a directory")
        with os.scandir(dname) as it:
            for entry in it:
                pth: str = entry.path
                if not entry.name.endswith(".json"):
                    continue
                if entry.is_file():
                    results.append(str(Path(pth).absolute()))
    output_dict = dict(name=name, json_list=results)
    return _out(output_dict)
