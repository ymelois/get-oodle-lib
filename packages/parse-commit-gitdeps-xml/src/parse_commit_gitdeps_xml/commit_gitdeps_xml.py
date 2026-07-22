import gzip
import os
import urllib.request
from io import BufferedReader
from typing import Self

from parse_commit_gitdeps_xml.blob import Blob
from parse_commit_gitdeps_xml.file import File
from parse_commit_gitdeps_xml.hash import Hash
from parse_commit_gitdeps_xml.pack import Pack
from parse_commit_gitdeps_xml.stream_utils import StreamUtils


class CommitGitdepsXML:
    __file_path: str
    __file_reader: BufferedReader
    __stream_utils: StreamUtils
    __base_url: bytes

    __files_offset: int
    __blobs_offset: int
    __packs_offset: int

    def __init__(self, file_path: str):
        if file_path is None:
            raise ValueError("File path cannot be None")
        if not os.path.isfile(file_path):
            raise ValueError("File path does not exist")

        self.__file_path = file_path

    def __enter__(self) -> Self:
        self.__file_reader = open(self.__file_path, "rb")
        self.__stream_utils = StreamUtils(self.__file_reader)

        # Find the BaseUrl value
        self.__stream_utils.consume_until(b'BaseUrl="')
        self.__base_url = self.__stream_utils.read_until(b'"')

        # Find the Files tag offset
        self.__stream_utils.consume_until(b"<Files>")
        self.__files_offset = self.__file_reader.tell()

        # Find the Blobs tag offset
        self.__stream_utils.consume_until(b"<Blobs>")
        self.__blobs_offset = self.__file_reader.tell()

        # Find the Packs tag offset
        self.__stream_utils.consume_until(b"<Packs>")
        self.__packs_offset = self.__file_reader.tell()

        return self

    def __exit__(self, exception_type, exception_value, traceback) -> None:
        self.__file_reader.close()

    def __get_file(self, name: bytes) -> File:
        self.__file_reader.seek(self.__files_offset)
        self.__stream_utils.consume_until(b'Name="' + name)
        partial_name = self.__stream_utils.read_until(b'"')

        if partial_name != b"":
            raise ValueError("File not found")

        self.__stream_utils.consume_until(b'Hash="')
        blob_hash = self.__stream_utils.read_until(b'"')
        buffer = self.__stream_utils.read_until(b"/>")
        is_executable = b'IsExecutable="true"' in buffer

        return File(name, Hash(blob_hash), is_executable)

    def __get_blob(self, hash: bytes) -> Blob:
        self.__file_reader.seek(self.__blobs_offset)
        self.__stream_utils.consume_until(hash)
        self.__stream_utils.consume_until(b'Size="')
        size = int(self.__stream_utils.read_until(b'"'))
        self.__stream_utils.consume_until(b'PackHash="')
        pack_hash = self.__stream_utils.read_until(b'"')
        self.__stream_utils.consume_until(b'PackOffset="')
        pack_offset = int(self.__stream_utils.read_until(b'"'))

        return Blob(Hash(hash), size, Hash(pack_hash), pack_offset)

    def __get_pack(self, hash: bytes) -> Pack:
        self.__file_reader.seek(self.__packs_offset)
        self.__stream_utils.consume_until(hash)
        self.__stream_utils.consume_until(b'Size="')
        size = int(self.__stream_utils.read_until(b'"'))
        self.__stream_utils.consume_until(b'CompressedSize="')
        compressed_size = int(self.__stream_utils.read_until(b'"'))
        self.__stream_utils.consume_until(b'RemotePath="')
        remote_path = self.__stream_utils.read_until(b'"')

        return Pack(Hash(hash), size, compressed_size, remote_path)

    def find_file_names(self, name: bytes) -> list[bytes]:
        """
        Find all file names starting with a specific name

        :param name: The start of the file name
        :type name: bytes
        :return: A list of file names with the given name
        """
        if b'"' in name:
            raise ValueError("File name cannot contain double quotes")

        file_names = []
        self.__file_reader.seek(self.__files_offset)

        while True:
            self.__stream_utils.consume_until(b'Name="' + name)

            if self.__file_reader.tell() >= self.__blobs_offset:
                break

            partial_name = self.__stream_utils.read_until(b'"')
            file_names.append(name + partial_name)

        return file_names

    def get_file_url(self, file_path: bytes) -> tuple[bytes, int, int]:
        """
        Get the URL, the size and the pack offset of a file

        :param file_path: The file path
        :type file_path: bytes
        :return: The URL, the size and the pack offset of the file
        """
        file = self.__get_file(file_path)
        blob = self.__get_blob(bytes(file.hash))
        pack = self.__get_pack(bytes(blob.pack_hash))

        url = self.__base_url + b"/" + pack.remote_path + b"/" + bytes(blob.pack_hash)

        return url, blob.size, blob.pack_offset

    def fetch_file(self, file_path: bytes) -> bytes:
        """
        Fetch the content of a file

        :param file_path: The file path
        :type file_path: bytes
        :return: The content of the file
        """
        url, size, pack_offset = self.get_file_url(file_path)

        # Download the pack
        response = urllib.request.urlopen(url.decode())
        compressed = response.read()

        # Decompress the pack
        decompressed = gzip.decompress(compressed)

        return decompressed[pack_offset : pack_offset + size]
