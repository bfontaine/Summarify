# -*- coding: UTF-8 -*-

import requests
from summarify.parser import PageParser


class Summary:
    @classmethod
    def from_url(cls, url: str):
        r = requests.get(url)
        r.raise_for_status()
        return cls(markup=r.text, _url=url)

    @classmethod
    def from_html(cls, html: str, url=None):
        return cls(markup=html, _url=url)

    def __init__(self, markup, _url=None):
        p = PageParser(markup, url=_url)

        self.url = p.parse_url()
        self.title = p.parse_title()
        self.description = p.parse_description()
        self.language = p.parse_language()
        self.author = p.parse_author()
        self.publisher = p.parse_publisher()
        self.picture = p.parse_picture()
        self.excerpt = p.parse_excerpt()

    def __iter__(self):
        for attr in ("url", "title", "description", "language", "author",
                     "publisher", "picture", "excerpt"):
            value = getattr(self, attr)
            if value:
                yield attr, value
