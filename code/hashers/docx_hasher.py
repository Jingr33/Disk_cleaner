from pathlib import Path
from zipfile import is_zipfile
import docx
import re

from file_data.file_info import FileInfo
from hashers.doc_hasher import DocHasher

class DocxHasher(DocHasher):
    def __init__(self, sorter, logger):
        super().__init__(sorter, logger)

    def extract_text_hash(self, file_info : FileInfo) -> str:
        """Extract docx file, return simhash of a file."""
        path = file_info.get_path()
        text = None
        try:
            if DocxHasher.is_probably_valid_docx(path):
                doc = docx.Document(path)
                text =  self.normalize_text('\n'.join([para.text for para in doc.paragraphs]))
        except Exception as e:
            self.logger.add_to_corrupted(file_info, e)
        return self.extract_hash_from_text(text)

    def extract_image_hash(self, file_info : FileInfo):
        """Extract image hash from a file -> None in this case."""
        return super().extract_image_hash(file_info)
        
    def is_probably_valid_docx(path: Path) -> bool:
        """Check, if file is valid docx."""
        return path.suffix.lower() == '.docx' and is_zipfile(path)

    def normalize_text(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r'\s+', ' ', text)  # sjednotit mezery
        return text.strip()
