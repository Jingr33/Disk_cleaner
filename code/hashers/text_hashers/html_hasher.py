from bs4 import BeautifulSoup

from file_data.file_info import FileInfo
from hashers.text_hashers.text_hasher_base import TextHasherBase

class HtmlHasher(TextHasherBase):
    def __init__(self, sorter, logger):
        super().__init__(sorter, logger)

    def _extract_text(self, file_info : FileInfo) -> str:
        """Extract html code, count and return simhash of a file."""
        html_contetnt = ''
        try:
            soup = None
            with open(file_info.get_path(), 'r', encoding='utf-8', errors='ignore') as f:
                soup = BeautifulSoup(f, 'html.parser')
            html_contetnt = soup.get_text()
        except Exception as e:
            self.logger.add_to_corrupted(file_info, e)
        return html_contetnt
