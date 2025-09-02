from pathlib import Path
from zipfile import is_zipfile
import docx
import re

from hashers.text_hashers.text_hasher_base import TextHasherBase
from file_data.file_info import FileInfo

class WordHasher(TextHasherBase):
    def __init__(self, sorter, logger):
        super().__init__(sorter, logger)

    def _extract_text(self, file_info : FileInfo) -> str:
        """Extract docx file, return simhash of a file."""
        path = file_info.get_path()
        text = None
        self._handle_unsupported_doc_exception(file_info)
        try:
            if WordHasher.is_probably_valid_docx(path):
                doc = docx.Document(path)
                text =  self.normalize_text('\n'.join([para.text for para in doc.paragraphs]))
        except Exception as e:
            self._unhashable_file_exception(file_info, e)
        return text

    def is_probably_valid_docx(path: Path) -> bool:
        """Check, if file is valid docx."""
        return path.suffix.lower() == '.docx' and is_zipfile(path)

    def normalize_text(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def _handle_unsupported_doc_exception(self, file_info : FileInfo) -> bool:
        """Return true, if specified file is unsupported type .doc."""
        # skip .doc presentations
        if file_info.get_suffix() in ['.doc', '.docm']:
            self.logger.add_to_corrupted(file_info, 'Unsupport presentation type .doc')
            return True
        return False

    def _unhashable_file_exception(self, file_info : FileInfo, error : Exception) -> int:
            """Handle fail to hash file exception."""
            self.logger.add_to_corrupted(file_info, error)
            file_info.set_auto_removability(False)
            return None
