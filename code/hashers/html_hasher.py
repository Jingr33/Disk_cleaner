from bs4 import BeautifulSoup

from file_data.file_info import FileInfo
from hashers.text_hasher import TextHasher

class HtmlHasher(TextHasher):
    def __init__(self, sorter, logger):
        super().__init__(sorter, logger)

    def extract_text_hash(self, file_info : FileInfo) -> int:
        """Extract html code, count and return simhash of a file."""
        html_contetnt = ''
        try:
            soup = None
            with open(file_info.get_path(), 'r', encoding='utf-8', errors='ignore') as f:
                soup = BeautifulSoup(f, 'html.parser')
            html_contetnt = soup.get_text()
        except Exception as e:
            self.logger.add_to_corrupted(file_info, e)
        return self.extract_hash_from_text(html_contetnt)

    def extract_image_hash(self, file_info : FileInfo):
        """Extract image hash from a file -> None in this case."""
        return super().extract_image_hash(file_info)