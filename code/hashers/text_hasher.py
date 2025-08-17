from pathlib import Path
from simhash import Simhash

from hashers.hasher_base import HasherBase

class TextHasher(HasherBase):
    def __init__(self, sorter, logger):
        super().__init__(sorter, logger)

    def extract_hash(self, path: Path) -> int:
        """Extract text file, return simhash of a file."""
        text = None
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        return self.extract_hash_from_text(text)

    def extract_hash_from_text(self, text : str) -> int:
        """Count simhash from text."""
        if not text:
            return None
        return Simhash(text.split()).value
