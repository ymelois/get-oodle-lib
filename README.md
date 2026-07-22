# get-oodle-lib
A library for getting the oodle library from Unreal Engine source code.
Currently a wip, as the parser it used needs to be updated to be compatible with all versions of the git deps file.

## Dependencies
- `Commit.gitdeps.xml` file from Unreal Engine source code (found [here](https://github.com/EpicGames/UnrealEngine/blob/release/Engine/Build/Commit.gitdeps.xml)) which access can be granted by following the instructions at https://github.com/EpicGames/Signup.

## Usage
```bash
python get_oodle_lib [OPTIONS] GITDEPS_PATH
```

For more information, run `python get_oodle_lib --help`.

You can also install the package with `pipx install git+https://github.com/Tempo-Organization/get-oodle-lib` and run it with `get-oodle-lib`.
