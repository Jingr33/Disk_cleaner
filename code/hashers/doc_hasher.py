from pathlib import Path

from hashers.text_hasher import TextHasher

class DocHasher(TextHasher):
    def __init__(self, sorter, logger):
        super().__init__(sorter, logger)

    def extract_hash(self, path: Path) -> str:
        """Extract content of doc file, count and return simhash."""
        text = ''
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
        return self.extract_hash_from_text(text)