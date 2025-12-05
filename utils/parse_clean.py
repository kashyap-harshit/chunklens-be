from bs4 import BeautifulSoup


def parse_and_clean(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator=" ")

    clean_text = " ".join(text.split())

    return clean_text


