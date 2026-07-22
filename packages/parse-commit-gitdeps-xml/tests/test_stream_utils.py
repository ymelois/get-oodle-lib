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


def test_consume_until_finds_pattern_split_across_a_chunk_boundary():
    data = b'____Hash="'  # "Hash=\"" split across the first two 8-byte chunks
    stream = BytesIO(data)
    su = StreamUtils(stream, 8)

    su.consume_until(b'Hash="')

    assert stream.tell() == len(data)


def test_finds_pattern_in_a_short_final_chunk():
    data = b"deadbeef"  # exactly one chunk, terminator is in the short next one
    su = StreamUtils(BytesIO(data + b'"____'), 8)

    value = su.read_until(b'"')

    assert value == data
