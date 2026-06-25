from html.parser import HTMLParser
from urllib.request import urlopen


class QuotesParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.quotes = []
        self.authors = []
        self._current_tag = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        if tag == "span" and attrs.get("class") == "text":
            self._current_tag = "quote"
        elif tag == "small" and attrs.get("class") == "author":
            self._current_tag = "author"

    def handle_endtag(self, tag):
        if tag in {"span", "small"}:
            self._current_tag = None

    def handle_data(self, data):
        text = data.strip()

        if not text:
            return

        if self._current_tag == "quote":
            self.quotes.append(text)
        elif self._current_tag == "author":
            self.authors.append(text)


url = "https://quotes.toscrape.com"

with urlopen(url, timeout=10) as response:
    html = response.read().decode("utf-8")

parser = QuotesParser()
parser.feed(html)

for quote, author in zip(parser.quotes, parser.authors):
    print(f"{quote} - {author}")
