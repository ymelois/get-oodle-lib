from dataclasses import dataclass

from .hash import Hash


@dataclass
class Blob:
    hash: Hash
    size: int
    pack_hash: Hash
    pack_offset: int

    def __repr__(self) -> str:
        return f"Blob({self.hash!r}, {self.size!r}, {self.pack_hash!r}, {self.pack_offset!r})"
