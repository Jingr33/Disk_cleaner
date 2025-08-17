from pathlib import Path
from bs4 import BeautifulSoup

from hashers.text_hasher import TextHasher

class HtmlHasher(TextHasher):
    def __init__(self, sorter, logger):
        super().__init__(sorter, logger)

    def extract_hash(self, path: Path) -> int:
        """Extract html code, count and return simhash of a file."""
        html_contetnt = ''
        try:
            soup = None
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                soup = BeautifulSoup(f, "html.parser")
            html_contetnt = soup.get_text()
        except Exception as e:
            self.logger.add_to_corrupted(path)
        return self.extract_hash_from_text(html_contetnt)
