import os
from typing import IO


class StreamUtils:
    __stream: IO[bytes]
    __buffer_size: int

    def __init__(self, stream: IO[bytes], buffer_size: int = 1024 * 8):
        self.__stream = stream
        self.__buffer_size = buffer_size

    def read_until(self, pattern: bytes) -> bytes:
        carry_len = len(pattern) - 1

        buf = self.__stream.read(self.__buffer_size)
        if not buf:
            return buf

        view = buf
        while pattern not in view:
            chunk = self.__stream.read(self.__buffer_size)
            if not chunk:
                return buf

            view = buf[-carry_len:] + chunk if carry_len else chunk
            buf += chunk

        self.__stream.seek(-len(view) + view.find(pattern) + len(pattern), os.SEEK_CUR)
        return buf[: -1 - len(view) + view.find(pattern) + len(pattern)]

    def consume_until(
        self,
        pattern: bytes,
    ) -> None:
        carry_len = len(pattern) - 1

        buf = self.__stream.read(self.__buffer_size)
        if not buf:
            return

        while pattern not in buf:
            chunk = self.__stream.read(self.__buffer_size)
            if not chunk:
                return

            buf = buf[-carry_len:] + chunk if carry_len else chunk

        self.__stream.seek(-len(buf) + buf.find(pattern) + len(pattern), os.SEEK_CUR)
