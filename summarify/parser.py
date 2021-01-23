# -*- coding: UTF-8 -*-
from typing import Optional

from bs4 import BeautifulSoup


class PageParser:
    def __init__(self, markup: str, url: Optional[str] = None):
        self.soup = BeautifulSoup(markup, "html.parser")
        self.head = self.soup.find("head")
        self._url = url

        self._collect_meta_tags()

    def _collect_meta_tags(self):
        self.metas = {}
        if not self.head:
            return

        for el in self.head.findAll("meta"):
            key = None
            for attr in ("name", "property", "http-equiv"):
                if attr in el.attrs:
                    key = el.attrs[attr]
                    break

            value = el.attrs.get("content")
            if key and value:
                self.metas[key.lower()] = value

    def _first_meta(self, *names):
        for name in names:
            if name in self.metas:
                return self.metas[name]

    def _find_text(self, *args, **kwargs) -> Optional[str]:
        el = self.soup.find(*args, **kwargs)
        if el:
            return el.get_text().strip()
        return None

    def parse_title(self) -> Optional[str]:
        if self.head:
            # 1. <head><title>...</title></head>
            title = self._find_text("title")
            if title:
                return title

            # 2. meta og:title or twitter:title
            m = self._first_meta("og:title", "twitter:title", )
            if m:
                return m

        # 3. <h1 itemprop="title">...</h1>
        #    <h1 itemprop="headline">...</h1>
        h1s = self.soup.find_all("h1")
        if h1s:
            for h1 in h1s:
                for k, v in h1.attrs:
                    if k.lower() == "itemprop":
                        if v.lower() in {"title", "headline"}:
                            return h1.get_text()

            # 4. <h1>...</h1>
            return h1s[0].get_text()

        # 5. itemprop=title or headline
        for itemprop in ("title", "headline"):
            title = self._find_text(itemprop=itemprop)
            if title:
                return title

        # 6. <h2>...</h2>, <h3>...</h3>, ..., <h6>...</h6>
        for h_tag in ("h2", "h3", "h4", "h5", "h6"):
            title = self._find_text(h_tag)
            if title:
                return title
        return None

    def parse_url(self) -> Optional[str]:
        if self._url:
            return self._url

        # 1. meta og:url or twitter:url
        m = self._first_meta("og:url", "twitter:url")
        if m:
            return m

        # 2. link rel=canonical
        canonical_link = self.soup.find("link", rel="canonical")
        if canonical_link and "href" in canonical_link.attrs:
            return canonical_link.attrs["href"]

        return None

    def parse_description(self) -> Optional[str]:
        # 1. meta description, og:description, or twitter:description
        m = self._first_meta("description", "og:description",
                             "twitter:description")
        if m:
            return m

        # 2. itemprop=description
        return self._find_text(itemprop="description")

    def parse_language(self) -> Optional[str]:
        # 1. meta language, content-language, dc.language, or og:locale
        m = self._first_meta("language", "content-language", "dc.language",
                             "og:locale")
        if m:
            return m

        # 2. html lang or xml:lang attributes
        html = self.soup.find("html")
        for attr in ("lang", "xml:lang"):
            if attr in html.attrs:
                return html.attrs[attr]

        return None

    def parse_publisher(self) -> Optional[str]:
        # We might want to use "article:publisher" but it's used for FB URLs.
        m = self._first_meta("dc.publisher")
        if m:
            return m

        return self._find_text(itemprop="publisher")

    def parse_author(self) -> Optional[str]:
        m = self._first_meta("author")
        if m:
            return m

        return self._find_text(itemprop="author")

    # TODO use self._url or parse_url to get a full URL here
    def parse_picture(self) -> Optional[str]:
        if not self.head:
            return None

        m = self._first_meta("og:image", "twitter:image")
        if m:
            return m

        for link in self.head.find_all("link"):
            rel = link.attrs.get("rel", "")
            href = link.attrs.get("href", "")
            if not rel or not href:
                continue

            rel = set(rel)

            # We might want to exploit attributes like sizes="72x72"
            # TODO only use "icon" if that's the only one available
            if rel & {"apple-touch-icon-precomposed", "apple-touch-icon",
                      "icon", "fluid-icon"}:
                return href

        # Also:
        # <figure class="illustration_haut   " style="width: 534px">
        #     <img width="534" data-lazyload="false" src="..."/>
        return None

    def parse_excerpt(self) -> Optional[str]:
        return None
        # Excerpt (content)
        # <div id="articleBody" class="contenu_article js_article_body"
        #      itemprop="articleBody">...</div>
