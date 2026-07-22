import re


class Hash:
    __internal: bytes
    __int: int

    def __init__(self, value: bytes):
        if len(value) != 40:
            raise ValueError("Hash must be 40 characters long")
        if not re.match(rb"^[0-9a-fA-F]+$", value):
            raise ValueError("Hash must be a hexadecimal string")
        self.__internal = value
        self.__int = int(value, 16)

    def __bytes__(self) -> bytes:
        return self.__internal

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Hash):
            return NotImplemented
        return self.__int == other.__int

    def __repr__(self) -> str:
        return f"Hash({self.__internal!r})"

    def __hash__(self) -> int:
        return self.__int
