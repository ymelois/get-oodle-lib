from io import BytesIO

from parse_commit_gitdeps_xml.stream_utils import StreamUtils


def test_reads_value_after_prefix():
    su = StreamUtils(BytesIO(b'<File Hash="deadbeef" />'))

    su.consume_until(b'Hash="')
    value = su.read_until(b'"')

    assert value == b"deadbeef"


def test_reads_second_value_after_first():
    su = StreamUtils(BytesIO(b'<A Hash="firsthash" /><B Hash="secondhash" />'))

    su.consume_until(b'Hash="')
    first = su.read_until(b'"')
    su.consume_until(b'Hash="')
    second = su.read_until(b'"')

    assert first == b"firsthash"
    assert second == b"secondhash"
