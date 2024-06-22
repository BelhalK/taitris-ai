from __future__ import annotations

from typing import Generator, Optional
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from pydantic import BaseModel

class WebPage(BaseModel):
    inner_text: str
    html: str
    url: str

    class Config:
        underscore_attrs_are_private = True

    _soup: Optional[BeautifulSoup] = None
    _title: Optional[str] = None

    @property
    def soup(self) -> BeautifulSoup:
        """
        Lazily initializes and returns the BeautifulSoup object for the HTML content.
        """
        if self._soup is None:
            self._soup = BeautifulSoup(self.html, "html.parser")
        return self._soup

    @property
    def title(self) -> str:
        """
        Lazily initializes and returns the title of the web page.
        """
        if self._title is None:
            title_tag = self.soup.find("title")
            self._title = title_tag.text.strip() if title_tag is not None else ""
        return self._title

    def get_links(self) -> Generator[str, None, None]:
        """
        Extracts and yields all valid links (absolute URLs) found in the HTML content.
        """
        for i in self.soup.find_all("a", href=True):
            url = i["href"]
            result = urlparse(url)
            if not result.scheme and result.path:
                yield urljoin(self.url, url)
            elif url.startswith(("http://", "https://")):
                yield urljoin(self.url, url)

def get_html_content(page: str, base: str) -> str:
    """
    Returns the stripped inner text content from the given HTML page.
    """
    soup = _get_soup(page)
    return soup.get_text(strip=True)

def _get_soup(page: str) -> BeautifulSoup:
    """
    Creates and returns a BeautifulSoup object, removing non-visible elements.
    """
    soup = BeautifulSoup(page, "html.parser")
    # Remove style, script, and other non-visible elements
    for s in soup(["style", "script", "[document]", "head", "title"]):
        s.extract()
    return soup