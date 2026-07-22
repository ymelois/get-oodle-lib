import pytest

from get_oodle_lib.common import parser


def test_parses_required_platform_and_gitdeps():
    args = parser.parse_args(["-p", "linux", "path/to/Commit.gitdeps.xml"])

    assert args.platform == "linux"
    assert args.gitdeps == "path/to/Commit.gitdeps.xml"
    assert args.output == "."


def test_rejects_unknown_platform():
    with pytest.raises(SystemExit):
        parser.parse_args(["-p", "unknown", "path/to/Commit.gitdeps.xml"])
