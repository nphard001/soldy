"""
soldy.path: WayMage, the master of path routing.
"""

from __future__ import annotations
import os
import json
from pathlib import Path


class WayMage:
    @classmethod
    def get_main_json(cls) -> str:
        """
        It's ~/.soldapi/main.json, but respect environment variable SOLDAPI_MAIN if set.
        """
        SOLDAPI_MAIN = os.environ.get("SOLDAPI_MAIN", None)
        if SOLDAPI_MAIN is None:
            return str(Path.home() / ".soldapi" / "main.json")
        
        p = Path(SOLDAPI_MAIN)
        if not p.exists():
            raise FileNotFoundError(f"SOLDAPI_MAIN file does not exist: {SOLDAPI_MAIN}")
        if not str(p).endswith(".json"):
            raise ValueError(f"SOLDAPI_MAIN supposed to be a .json file, got: {SOLDAPI_MAIN}")

        return str(p)

    @classmethod
    def solve(cls, dot_path: str, base: str | Path | None = None) -> str:
        """
        Resolve a dot-path by hopping through JSON config files
        Each non-terminal segment must resolve to a .json file to keep hopping
        """
        if base is None:
            base = cls.get_main_json()

        parts = dot_path.split(".")
        current_path = Path(base)
        current_data = json.loads(cls.read(current_path))
        for i, key in enumerate(parts):
            
            # Rule1: Last part treat as it is.
            value = current_data[key]
            if key not in current_data:
                raise KeyError(f"Key '{key}' not found in {current_path}")
                
            is_last = (i == len(parts) - 1)
            if is_last:
                return value

            # Rule2: Mid-path must resolve to a .json file
            if not value.endswith(".json"):
                raise ValueError(
                    f"Mid-path key '{key}' resolved to a non-JSON value '{value}'; "
                    f"intermediate hops must point to a .json config file"
                )

            current_path = Path(value)
            current_data = json.loads(cls.read(current_path))

        # Unreachable: last value will be returned anyway
        raise AssertionError(f"solve() fell through for {dot_path!r}")

    @classmethod
    def read(cls, pth: str | Path) -> str:
        """
        Read file as UTF-8 with BOM tolerance (utf-8-sig)
        """
        return Path(pth).read_text(encoding="utf-8-sig")
