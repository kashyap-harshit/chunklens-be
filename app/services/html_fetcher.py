import requests
from bs4 import BeautifulSoup
from typing import Tuple
from urllib.parse import urlparse


class HTMLFetcher:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    def fetch_and_parse(self, url: str) -> Tuple[BeautifulSoup, str]:

        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "lxml")

            # Remove script, style, and other non-content tags
            for tag in soup(["script", "style", "meta", "link", "noscript", "iframe"]):
                tag.decompose()

            # Get path from URL
            parsed_url = urlparse(url)
            path = parsed_url.path or "/home"

            return soup, path

        except requests.exceptions.RequestException as e:
            raise Exception(f"Error fetching URL: {str(e)}")

    def extract_text_with_structure(self, soup: BeautifulSoup) -> list:

        chunks = []

        for element in soup.find_all(
            ["p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "div"]
        ):
            text = element.get_text(strip=True)
            if text and len(text) > 20:
                html_preview = str(element)[:200]
                chunks.append(
                    {"text": text, "html_preview": html_preview, "tag": element.name}
                )

        return chunks
