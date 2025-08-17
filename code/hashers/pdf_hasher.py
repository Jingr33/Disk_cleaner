from pathlib import Path
import fitz
import io
from PIL import Image

from hashers.text_hasher import TextHasher
from hashers.image_hasher import ImageHasher
from console_writer import ConsoleWriter
from decorators import suppress_stderr

class PdfHasher(TextHasher, ImageHasher):
    def __init__(self, sorter, logger):
        super().__init__(sorter, logger)

    def extract_hash(self, path: Path) -> int:
        """Extract percentual simhash from pdf file. 
        From text, if it is possible, if not, count image pahsh."""
        with suppress_stderr():
            try:
                text = self.extract_text_fom_pdf(path)
                simhash = self.extract_hash_from_text(text)
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
                combined_hash ^= self.get_phash_value(img)
        return combined_hash
