from pathlib import Path
from zipfile import is_zipfile
import docx

from file_data.file_info import FileInfo
from hashers.doc_hasher import DocHasher

class DocxHasher(DocHasher):
    def __init__(self, sorter, logger):
        super().__init__(sorter, logger)

    def extract_hash(self, file_info : FileInfo) -> str:
        """Extract docx file, return simhash of a file."""
        path = file_info.get_path()
        text = None
        try:
            if DocxHasher.is_probably_valid_docx(path):
                doc = docx.Document(path)
                text =  "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            self.logger.add_to_corrupted(file_info, e)
        return self.extract_hash_from_text(text)
        
    def is_probably_valid_docx(path: Path) -> bool:
        """Check, if file is valid docx."""
        return path.suffix.lower() == ".docx" and is_zipfile(path)
