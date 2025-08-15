from pathlib import Path
from zipfile import is_zipfile
import docx

from text_hasher import TextHasher

class DocHasher(TextHasher):
    def __init__(self):
        ...

    def extract_docx_file(self, path: Path) -> str:
        """Extract docx file, return simhash of a file."""
        text = None
        try:
            if DocHasher.is_probably_valid_docx(path):
                doc = docx.Document(path)
                text =  "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            self.logger.add_to_corrupted(path)
        return self._get_simhash_from_text(text)
        
    def extract_doc_file(self, path: Path) -> str:
        """Extract content of doc file, count and return simhash."""
        text = None
        pass
        # try:
        #     word = win32com.client.Dispatch("Word.Application")
        #     word.Visible = False
        #     doc = word.Documents.Open(str(path))
        #     try:
        #         text = doc.Content.Text
        #     finally:
        #         doc.Close(False)
        #         word.Quit()

        #     cleaned_text = text.strip().replace("\r", "").replace("\n", "")
        #     return hashlib.sha256(cleaned_text.encode('utf-8')).hexdigest()
        
        # except Exception as e:
        #     self.logger.add_to_corrupted(path)
        #     return ""
        return self._get_simhash_from_text(text)

    def is_probably_valid_docx(path: Path) -> bool:
        """Check, if file is valid docx."""
        return path.suffix.lower() == ".docx" and is_zipfile(path)
