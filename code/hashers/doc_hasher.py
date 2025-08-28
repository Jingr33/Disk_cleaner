from file_data.file_info import FileInfo
from hashers.text_hasher import TextHasher

class DocHasher(TextHasher):
    def __init__(self, sorter, logger):
        super().__init__(sorter, logger)

    def extract_text_hash(self, file_info : FileInfo) -> str:
        """Extract content of doc file, count and return simhash."""
        text = ''
        self.logger.add_to_corrupted(file_info, 'Unsupport word type .doc')
        return self.extract_hash_from_text(text)

    def extract_image_hash(self, file_info : FileInfo):
        """Extract image hash from a file -> None in this case."""
        return super().extract_image_hash(file_info)