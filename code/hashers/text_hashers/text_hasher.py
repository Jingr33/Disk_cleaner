from file_data.file_info import FileInfo
from hashers.text_hashers.text_hasher_base import TextHasherBase

class TextHasher(TextHasherBase):
    def __init__(self, sorter, logger):
        super().__init__(sorter, logger)

    def _extract_text(self, file_info : FileInfo) -> str:
        """Extract text file, return simhash of a file."""
        path = file_info.get_path()
        text = None
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        return text
