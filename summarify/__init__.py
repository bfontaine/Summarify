# -*- coding: UTF-8 -*-

__version__ = "0.0.2"

from typing import Optional

from summarify.summary import Summary


def from_url(url: str):
    return Summary.from_url(url)


def from_html(markup: str, url: Optional[str] = None):
    return Summary.from_html(markup, url=url)
