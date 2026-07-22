import os
from io import BufferedReader


class StreamUtils:
    __stream: BufferedReader
    __buffer_size: int = 1024 * 8

    def __init__(self, stream: BufferedReader):
        self.__stream = stream

    def __st_size(self) -> int:
        initial_position = self.__stream.tell()
        self.__stream.seek(0, os.SEEK_END)
        size = self.__stream.tell()
        self.__stream.seek(initial_position)
        return size

    def read_until(self, pattern: bytes) -> bytes:
        buffer = self.__stream.read(self.__buffer_size)
        if not buffer:
            return buffer

        iterations = 0
        while pattern not in buffer[iterations * self.__buffer_size :]:
            iterations += 1
            buffer += self.__stream.read(self.__buffer_size)
            if len(buffer[iterations * self.__buffer_size :]) < self.__buffer_size:
                return buffer

        pattern_index = buffer[iterations * self.__buffer_size :].find(pattern)
        self.__stream.seek(-(self.__buffer_size - pattern_index - len(pattern)), os.SEEK_CUR)
        return buffer[: iterations * self.__buffer_size + pattern_index]

    def consume_until(
        self,
        pattern: bytes,
    ) -> None:
        buffer = self.__stream.read(self.__buffer_size)
        if not buffer:
            return

        while pattern not in buffer:
            buffer = self.__stream.read(self.__buffer_size)
            if not buffer:
                return

        self.__stream.seek(-self.__buffer_size, os.SEEK_CUR)
        self.read_until(pattern)
