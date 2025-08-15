from pathlib import Path
import fitz
import io
from PIL import Image
import imagehash

from text_hasher import TextHasher
from console_writer import ConsoleWriter
from decorators import suppress_stderr

class PdfHasher(TextHasher):
    def __init__():
        ...

    def extract_pdf_file(self, path: Path) -> int:
        """Extract percentual simhash from pdf file. 
        From text, if it is possible, if not, count image pahsh."""
        with suppress_stderr():
            try:
                text = self.extract_text_fom_pdf(path)
                simhash = self._get_simhash_from_text(text)
                if simhash:
                    return simhash
                return self.extract_hash_from_pdf_as_image(path)
            except Exception as e:
                ConsoleWriter.faild_to_read_pdf(path, e)
                return None

    def extract_text_fom_pdf(self, path : Path) -> int:
        """Extract text from PDF file."""
        text = ""
        with fitz.open(path) as pdf:
            for page in pdf:
                extracted = page.get_text()
                if extracted:
                    text += extracted + "\n"
        return text

    def extract_hash_from_pdf_as_image(self, path : Path) -> int:
        """Count phash from pdf file as from image. """
        combined_hash = 0
        with fitz.open(path) as pdf:
            for i, page in enumerate(pdf):
                if i >= 10:
                    break        
                pix = page.get_pixmap(dpi=150)
                img = Image.open(io.BytesIO(pix.tobytes()))
                phash_val = int(str(imagehash.phash(img)), 16)
                combined_hash ^= phash_val
        return combined_hash
