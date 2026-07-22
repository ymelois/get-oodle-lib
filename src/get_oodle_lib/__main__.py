import os
from pathlib import Path

from parse_commit_gitdeps_xml import CommitGitdepsXML

from get_oodle_lib.common import parser


def main():
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

    platform_map = {
        "windows": "Win64",
        "linux": "Linux",
        "mac": "Mac",
    }

    # Parse the Commit.gitdeps.xml
    with CommitGitdepsXML(args.gitdeps) as gitdeps:
        file_prefix = b"Engine/Source/Runtime/OodleDataCompression/Sdks/"
        file_paths = gitdeps.find_file_names(file_prefix)

        get_version = lambda name: tuple(
            map(int, name[len(file_prefix) :].split(b"/", 1)[0].split(b"."))
        )

        # Get the latest version of the library
        versions = [get_version(file_path) for file_path in file_paths]
        latest_version = max(versions)
        latest_version_text = ".".join(map(str, latest_version)).encode()

        # Get the latest files
        latest_files = [
            file_path
            for file_path in file_paths
            if file_path[len(file_prefix) :].startswith(latest_version_text)
        ]

        # Get the libraries for the target platform
        target_libraries = [
            file_path
            for file_path in latest_files
            if file_path[
                len(file_prefix) + len(latest_version_text) + 1 :
            ].startswith(b"lib/" + platform_map[args.platform].encode() + b"/")
        ]

        for file_path in target_libraries:
            file_name = file_path.rsplit(b"/", 1)[-1].decode()

            with open(f"{args.output}/{file_name}", "wb") as f:
                print(f"Writing {file_name}...")
                f.write(gitdeps.fetch_file(file_path))


if __name__ == "__main__":
    main()
