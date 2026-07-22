# `Commit.gitdeps.xml` parser

This is a fast parser for the `Commit.gitdeps.xml` file from Unreal Engine source code (found [here](https://github.com/EpicGames/UnrealEngine/blob/release/Engine/Build/Commit.gitdeps.xml)) which access can be granted by following the instructions at https://github.com/EpicGames/Signup.

## Usage

```python
file_path = b"Engine/Source/Runtime/OodleDataCompression/Sdks/2.9.10/lib/Linux/liboo2corelinux64.so.9"

with CommitGitdepsXML("Commit.gitdeps.xml") as gitdeps:
    with(open("liboo2corelinux64.so.9", "wb")) as file:
        file.write(gitdeps.fetch_file(file_path))
```
