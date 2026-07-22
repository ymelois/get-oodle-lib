# get-oodle-lib

A library for getting the oodle library from Unreal Engine source code.

## Dependencies

- `Commit.gitdeps.xml` file from Unreal Engine source code (found [here](https://github.com/EpicGames/UnrealEngine/blob/release/Engine/Build/Commit.gitdeps.xml)) which access can be granted by following the instructions at https://github.com/EpicGames/Signup.

## Install

```bash
# Install it either from PyPI or GitHub
uv tool install get_oodle_lib@latest
uv tool install git+https://github.com/sehnryr/get-oodle-lib
# then run
get_oodle_lib --help
# Or use uvx
uvx get_oodle_lib@latest --help
uvx --from git+https://github.com/sehnryr/get-oodle-lib get-oodle-lib --help
```

## Usage

```
> get-oodle-lib --help
usage: get_oodle_lib [-h] -p {windows,linux,mac} [-o OUTPUT] gitdeps

Get Oodle library for Unreal Engine

positional arguments:
  gitdeps               Path to Commit.gitdeps.xml

options:
  -h, --help            show this help message and exit
  -p, --platform {windows,linux,mac}
                        Target platform to download the Oodle library for
  -o, --output OUTPUT   Path to output directory
```

## Development

Either use the Nix flake development shell or install python and uv manually, then:

```bash
uv sync
uv run get-oodle-lib --help
```

## License

This project and its packages are licensed under either of [`Apache License 2.0`](LICENSE-APACHE) or [`MIT License`](LICENSE-MIT) at your option.
