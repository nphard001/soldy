"""
simple SOLD model: The TextDealer
"""


import os
import sys
import json
import secrets
# import anyio
import diskcache  # NO orjson
import click  # NO typer, NO Pydantic
import psutil
from pathlib import Path


class NTMage:
    """
    N2-related utilities, slug with for Human-Friendly Identifiers
    """
    @classmethod
    def get_slug(cls, n: int = 2) -> str:
        """
        By default it's n=2, i.e. CVCVDDDD slug.
        For example, n=1 like go87, n=2 like love5566.
        """
        set1_C = "bcdfghjklmnpqrstvwxyz"
        set2_V = "aeiou"
        set3_D = "123456789"  # NO zero (for some reason)
        cv = ''.join(secrets.choice(set1_C) + secrets.choice(set2_V) for _ in range(n))
        dd = ''.join(secrets.choice(set3_D) for _ in range(n * 2))
        return cv + dd
    
    @classmethod
    def get_ns(cls) -> int:
        """
        Get current Unix timestamp in nanoseconds.
        """
        return psutil.time.time_ns()
    
    @classmethod
    def cover_tail(cls, long_str: str, short_str: str) -> str:
        """
        Cover the tail of a long string with a short string.
        Example:
            cover_tail(str(now_ns), 'love5566')
            '17760094721love5566'
        """
        if len(short_str) > len(long_str):
            raise ValueError("Short string cannot be longer than long string.")
        return long_str[:-len(short_str)] + short_str

class SoldText:
    def __init__(self, name: str, text: str, *, tl: int | None = None, td: str | None = None):
        self.name = name
        self.text = text
        self.tl: int = NTMage.get_ns() if tl is None else tl
        self.td: str = NTMage.get_slug() if td is None else td

    def to_sold(self) -> list[dict, dict, int, str]:
        ts = dict(name=self.name)
        to = dict(text=self.text)  # You definitely can do this.
        tsold = [ts, to, self.tl, self.td]
        return tsold
    
    @property
    def addr(self) -> str:
        return NTMage.cover_tail(str(self.tl), self.td)
    
    def save(self, pth: str | Path) -> int:
        return SoldText.soldapi_save(self, pth)

    @classmethod
    def soldapi_save(cls, soldy, pth: str | Path) -> int:
        sold_json = json.dumps(soldy.to_sold(), indent=1, ensure_ascii=False)
        sold_file = soldy.addr + ".json"
        p = Path(pth) / sold_file
        return p.write_text(sold_json, encoding="utf-8")
    
    @classmethod
    def soldapi_load(cls, pth: str | Path) -> list[dict, dict, int, str]:
        sold_json = Path(pth).read_text(encoding="utf-8-sig")
        ts, to, tl, td = json.loads(sold_json)
        real_to = ts.copy()
        real_to.update(to)
        if not isinstance(tl, int):
            raise TypeError(f"Invalid SoldText: L must be an integer, got {type(tl).__name__}")
        if not isinstance(td, str) or len(td) < 1:
            raise ValueError(f"Invalid SoldText: D must be a non-empty string, got {td!r}")
        return [ts, real_to, tl, td]

class TextDealer:  # It deals with SoldText objects, the broker between SOLD format and real I/O.
    pass