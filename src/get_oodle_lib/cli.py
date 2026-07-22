from get_oodle_lib import initialization, oodle_lib_core, data_structures

import rich_click as click
from pathlib import Path


# later have an option to auto download the git deps file and allow version specification


platform_choices = data_structures.get_enum_strings_from_enum(
    data_structures.Platform,
)

@click.command()
@click.version_option()
@click.option(
    "--output",
    type=click.Path(exists=True, resolve_path=True, path_type=Path),
    default='.',
    help="Path to a directory to have the oodle lib outputted to. Defaults to the current working directory."
)
@click.argument(
    "gitdeps-path",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        path_type=Path,
    ),
    required=True,
    help="Path to your git deps file.",
)
@click.option(
    "--platform",
    type=click.Choice(platform_choices),
    help="The platform type of oodle lib to download. Defaults to windows.",
    default=platform_choices[0], # windows, later default to machine os.
)
def cli(
    output: Path,
    gitdeps_path: Path,
    platform: str,
    max_content_width: int = 200
):
    initialization.initialization()
    platform_choice = data_structures.get_enum_from_val(data_structures.Platform, platform)
    get_oodle_lib(output, gitdeps_path, platform_choice)


def get_oodle_lib(output: Path, gitdeps_path: Path, platform: data_structures.Platform):
    initialization.initialization()
    oodle_lib_core.get_oodle_lib(output, gitdeps_path, platform)
