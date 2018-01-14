# -*- coding: UTF-8 -*-

__version__ = "0.0.1"

from summarify.summary import Summary

def from_url(url):
    return Summary.from_url(url)

def from_html(markup):
    return Summary.from_html(markup)
