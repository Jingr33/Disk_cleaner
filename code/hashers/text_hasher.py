from simhash import Simhash

from file_data.file_info import FileInfo
from hashers.hasher_base import HasherBase

class TextHasher(HasherBase):
    def __init__(self, sorter, logger):
        super().__init__(sorter, logger)

    def extract_text_hash(self, file_info : FileInfo) -> int:
        """Extract text file, return simhash of a file."""
        path = file_info.get_path()
        text = None
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        return self.extract_hash_from_text(text)

    def extract_image_hash(self, file_info : FileInfo) -> int:
        """Extract image phash from file -> None in this case."""
        return super().extract_image_hash(file_info)

    def extract_hash_from_text(self, text : str) -> int:
        """Count simhash from text."""
        if not text:
            return None
        return Simhash(text.split()).value
