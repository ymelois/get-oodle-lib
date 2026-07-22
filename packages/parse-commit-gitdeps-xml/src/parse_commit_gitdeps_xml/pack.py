from dataclasses import dataclass

from .hash import Hash


@dataclass
class Pack:
    hash: Hash
    size: int
    compressed_size: int
    remote_path: bytes

    def __repr__(self) -> str:
        return f"Pack({self.hash!r}, {self.size!r}, {self.compressed_size!r}, {self.remote_path!r})"
