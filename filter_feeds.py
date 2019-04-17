from typing import Callable

import requests

from bs4 import BeautifulSoup as Soup

FilterFunc = Callable[[Soup], bool]


def newyorker(item: Soup) -> bool:
    return not item.link.text.startswith("https://www.newyorker.com/magazine/")


def nybooks(item: Soup) -> bool:
    return not item.guid.text.startswith("https://www.nybooks.com/articles/")


def guardian(item: Soup) -> bool:
    url = item.link.text
    sport = url.startswith("https://www.theguardian.com/sport/")
    football = url.startswith("https://www.theguardian.com/football/")

    return sport or football


FEEDS = {
    "newyorker": ("https://www.newyorker.com/feed/magazine/rss", newyorker),
    "nybooks": ("https://feeds.feedburner.com/nybooks", nybooks),
    "guardian": ("https://www.theguardian.com/international/rss", guardian),
}


def get_feed(url: str) -> str:
    r = requests.get(url, timeout=5)
    return r.text


def filter_feed(url: str, filter_func: FilterFunc) -> str:
    xml = get_feed(url)
    soup = Soup(xml, "xml")

    for item in soup.find_all("item"):
        if filter_func(item):
            item.decompose()

    return str(soup)
