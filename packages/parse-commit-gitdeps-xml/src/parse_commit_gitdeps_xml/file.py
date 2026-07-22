from dataclasses import dataclass

from .hash import Hash


@dataclass
class File:
    name: bytes
    hash: Hash
    is_executable: bool

    def __repr__(self) -> str:
        return f"File({self.name!r}, {self.hash!r}, {self.is_executable!r})"
