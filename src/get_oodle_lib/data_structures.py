from enum import Enum
from typing import Type, TypeVar


platform_map = {
    "windows": "Win64",
    "linux": "Linux",
    "mac": "Mac",
}


class Platform(Enum):
    """
    Enum for which platform to get the oodle lib for.
    """
    WINDOWS = 'windows'
    LINUX = 'linux'
    MAC = 'mac'


E = TypeVar("E", bound=Enum)

def get_enum_from_val[E: Enum](enum_cls: type[E], value: object) -> E:
    for entry in enum_cls:
        if entry.value == value:
            return entry
    raise ValueError(f"{value} is not a valid value for {enum_cls.__name__}")


def get_enum_strings_from_enum(enum_cls: Type[Enum]) -> list[str]:
    return [entry.value for entry in enum_cls]
