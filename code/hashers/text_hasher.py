from pathlib import Path
from simhash import Simhash

from hasher import Hasher

class TextHasher(Hasher):
    def __init__(self):
        ...

    def _get_simhash_from_text(self, text : str) -> int:
        """Count simhash from text."""
        if not text:
            return None
        return Simhash(text.split()).value

    def extract_text_file(self, path: Path) -> int:
        """Extract text file, return simhash of a file."""
        text = None
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        return self._get_simhash_from_text(text)

