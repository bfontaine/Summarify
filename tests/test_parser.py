from summarify.parser import PageParser


def test_empty():
    p = PageParser("")
    assert p.parse_url() is None
    assert p.parse_title() is None
    assert p.parse_description() is None
    assert p.parse_language() is None
    assert p.parse_author() is None
    assert p.parse_publisher() is None
    assert p.parse_picture() is None
    assert p.parse_excerpt() is None
