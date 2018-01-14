# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup



class Summary:
    @classmethod
    def from_url(cls, url):
        r = requests.get(url)
        r.raise_for_status()
        return cls(markup=r.text, _url=url)

    @classmethod
    def from_html(cls, html):
        return cls(markup=html)

    def __init__(self, markup, _url=None):
        self.url = _url

        self._parse(BeautifulSoup(markup, "html.parser"))

    def _parse(self, soup):
        self.title = None
        self.description = None
        self.excerpt = None
        self.picture = None

        head = soup.find("head")
        metas = _collect_meta_tags(head)

        # Title
        def parse_title():
            if head:
                # 1. <head><title>...</title></head>
                title = head.find("title")
                if title:
                    return title.get_text()

                # 2. meta og:title or twitter:title
                for m in ("og:title","twitter:title",):
                    if m in metas:
                        return metas[m]

            # 3. <h1 itemprop="headline">...</h1>
            h1s = soup.find_all("h1")
            if h1s:
                for h1 in h1s:
                    for k, v in h1.attrs:
                        if k.lower() == "itemprop" and v.lower() == "headline":
                            return h1.get_text()

                # 4. <h1>...</h1>
                return h1s[0].get_text()

            # 5. <h2>...</h2>, <h3>...</h3>, (...), <h6>...</h6>
            for h_tag in ("h2", "h3", "h4", "h5", "h6"):
                h = soup.find(h_tag)
                if h:
                    return h.get_text()

        self.title = parse_title()

        # URL
        def parse_url():
            # 1. meta og:url or twitter:url
            for m in ("og:url", "twitter:url"):
                if m in metas:
                    return metas[m]

            # 2. link rel=canonical
            canonical_link = soup.find("link", rel="canonical")
            if canonical_link and "href" in canonical_link.attrs:
                return canonical_link.attrs["href"]

        if not self.url:
            self.url = parse_url()

        # Description
        def parse_description():
            # 1. meta description, og:description, or twitter:description
            for m in ("description", "og:description", "twitter:description"):
                if m in metas:
                    return metas[m]

            # 2. itemprop=description
            description = soup.find(itemprop="description")
            if description:
                return description

        self.description = parse_description()

        # Language
        def parse_language():
            x

        # Language
        # <meta name="DC.language" content="fr">
        # <meta property="og:locale" content="fr_FR" />

        # Publisher
        # <meta name="DC.publisher" content="Le Monde">
        # <span id="publisher" itemprop="Publisher">Le Monde</span>

        # Author
        # <span itemprop="author">...</span>
        # <meta name="author"      content="..."/>

        # Icon
        # <link rel="apple-touch-icon-precomposed" sizes="72x72" href="//s1.lemde.fr/medias/web/1.2.705/ico/apple/icon-72.png">
        # <link rel="apple-touch-icon-precomposed" sizes="144x144" href="//s1.lemde.fr/medias/web/1.2.705/ico/apple/icon-144.png">
        # <link rel="apple-touch-icon"      href="i/apple.png" />
        # <link rel="icon" type="image/png" href="i/favicon.png" />
        # <meta property="og:image" content="..."/>
        # <meta name="twitter:image" content="..."/>
        # <link rel="shortcut icon" href="..."/>
        # + /favicon.ico?

        # Image
        # <figure class="illustration_haut   " style="width: 534px">
        #     <img width="534" data-lazyload="false" src="..."/>

        # Excerpt (content)
        # <div id="articleBody" class="contenu_article js_article_body"
        #      itemprop="articleBody">...</div>
