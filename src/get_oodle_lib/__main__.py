import argparse
import os
from enum import StrEnum
from pathlib import Path

from parse_commit_gitdeps_xml import CommitGitdepsXML


class Platform(StrEnum):
    canonical: str

    WINDOWS = "windows", "Win64"
    LINUX = "linux", "Linux"
    MAC = "mac", "Mac"

    def __new__(cls, value: str, canonical: str) -> "Platform":
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.canonical = canonical
        return obj


class File:
    prefix: bytes
    path: bytes

    def __init__(self, prefix: bytes, path: bytes) -> None:
        self.prefix = prefix
        self.path = path

    def get_path(self) -> bytes:
        return self.path

    def get_name(self) -> str:
        return self.path.rsplit(b"/", 1)[-1].decode()

    def get_version(self) -> tuple[int, ...]:
        raw_version = self.path[len(self.prefix) :].split(b"/", 1)[0]
        return tuple(map(int, raw_version.split(b".")))

    def is_version(self, version: tuple[int, ...]) -> bool:
        return version == self.get_version()

    def is_platform(self, platform: Platform) -> bool:
        raw_platform = self.path[len(self.prefix) :].split(b"/", 3)[2]
        return platform.canonical.encode() == raw_platform


def main():
    parser = argparse.ArgumentParser(
        prog="get_oodle_lib",
        description="Get Oodle library for Unreal Engine",
    )

    parser.add_argument(
        "-p",
        "--platform",
        type=Platform,
        choices=list(Platform),
        help="Target platform to download the Oodle library for",
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Path to output directory",
        default=".",
    )
    parser.add_argument(
        "gitdeps",
        type=str,
        help="Path to Commit.gitdeps.xml",
    )

    args = parser.parse_args()

    # Check if the gitdeps's path is valid and exists
    if not os.path.isfile(args.gitdeps):
        print("Invalid path to Commit.gitdeps.xml")
        exit(1)

    # Check if the output path is valid and exists else create it
    if not os.path.isdir(args.output):
        try:
            path = Path(args.output)
            path.mkdir(parents=True)
        except OSError:
            print("Invalid path to output directory")
            exit(1)

    # Parse the Commit.gitdeps.xml
    with CommitGitdepsXML(args.gitdeps) as gitdeps:
        file_prefixes = [
            b"Engine/Source/Runtime/OodleDataCompression/Sdks/",
            b"Engine/Plugins/Compression/OodleData/Sdks/",
        ]

        files = [
            File(file_prefix, file_path)
            for file_prefix in file_prefixes
            for file_path in gitdeps.find_file_names(file_prefix)
        ]

        # Get the latest version of the library
        versions = map(lambda x: x.get_version(), files)
        latest_version = max(versions)

        # Get the latest files
        latest_files = filter(lambda x: x.is_version(latest_version), files)

        # Get the libraries for the target platform
        target_libraries = filter(lambda x: x.is_platform(args.platform), latest_files)

        for file in target_libraries:
            file_path = file.get_path()
            file_name = file.get_name()

            with open(f"{args.output}/{file_name}", "wb") as f:
                print(f"Writing {file_name}...")
                f.write(gitdeps.fetch_file(file_path))


if __name__ == "__main__":
    main()
