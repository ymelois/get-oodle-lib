import argparse

parser = argparse.ArgumentParser(
    prog="get_oodle_lib",
    description="Get Oodle library for Unreal Engine",
)
parser.add_argument(
    "-p",
    "--platform",
    type=str,
    choices=["windows", "linux", "mac"],
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
