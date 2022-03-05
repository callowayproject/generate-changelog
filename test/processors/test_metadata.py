"""Test the metadata collectors."""

from generate_changelog.processors import metadata

sample_msg_1 = """
This is a message body.

With multi-line content:
- one
- two

Bug: #42
Change-Id: Ic8aaa0728a43936cd4c6e1ed590e01ba8f0fbf5b
Signed-off-by: A. U. Thor <committer@example.com>
CC: R. E. Viewer <reviewer@example.com>
Subject: This is a fake subject spanning to several lines
  as you can see
"""


def test_parse_trailers():
    """Parse trailers should parse all trailers out of the message and store the data."""
    metadata_collector = metadata.MetadataCollector()
    parse_trailers = metadata.ParseTrailers(commit_metadata=metadata_collector)
    msg = parse_trailers(sample_msg_1)
    assert msg == sample_msg_1[:63]

    md = metadata_collector.metadata
    assert "trailers" in md
    assert len(md["trailers"]) == 5
    trailers = md["trailers"]
    assert trailers["bug"] == ["#42"]
    assert trailers["change-id"] == ["Ic8aaa0728a43936cd4c6e1ed590e01ba8f0fbf5b"]
    assert trailers["signed-off-by"] == ["A. U. Thor <committer@example.com>"]
    assert trailers["cc"] == ["R. E. Viewer <reviewer@example.com>"]
    assert trailers["subject"] == ["This is a fake subject spanning to several lines\nas you can see"]


def test_metadata_collector():
    """Metadata collector should collect metadata."""
    mdc = metadata.MetadataCollector()
    mdc(foo="bar")
    assert mdc.metadata == {"foo": "bar"}

    mdc = metadata.MetadataCollector({"foo": ["bar"]})
    assert mdc.metadata == {"foo": ["bar"]}

    mdc(foo=["bar"])
    assert mdc.metadata == {"foo": ["bar"]}

    mdc(foo=["baz"])
    assert set(mdc.metadata["foo"]) == {"baz", "bar"}
