from get_oodle_lib.data_structures import Platform, platform_map

from pathlib import Path

from parse_commit_gitdeps_xml import CommitGitdepsXML


def get_oodle_lib(output: Path, gitdeps_path: Path, platform: Platform) -> None:
    with CommitGitdepsXML(str(gitdeps_path)) as gitdeps:
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
            ].startswith(b"lib/" + platform_map[platform.value].encode() + b"/")
        ]

        for file_path in target_libraries:
            file_name = file_path.rsplit(b"/", 1)[-1].decode()

            with open(f"{output}/{file_name}", "wb") as f:
                print(f"Writing {file_name}...")
                f.write(gitdeps.fetch_file(file_path))
