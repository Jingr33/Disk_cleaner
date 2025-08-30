from file_data.file_info import FileInfo
from hashers.text_hashers.text_hasher_base import TextHasherBase

class DocHasher(TextHasherBase):
    def __init__(self, sorter, logger):
        super().__init__(sorter, logger)

    def _extract_text(self, file_info : FileInfo) -> str:
        """Extract content of doc file, count and return simhash."""
        text = ''
        self.logger.add_to_corrupted(file_info, 'Unsupport word type .doc')
        return text
