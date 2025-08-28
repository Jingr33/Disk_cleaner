from pathlib import Path
import fitz
fitz.TOOLS.mupdf_display_errors(False)
import io
from PIL import Image

from file_data.file_info import FileInfo
from hashers.text_hasher import TextHasher
from hashers.image_hasher import ImageHasher
from decorators import suppress_stderr
from config import PDF_IMAGE_MAX_PAGES

class PdfHasher(TextHasher, ImageHasher):
    def __init__(self, sorter, logger):
        super().__init__(sorter, logger)

    def extract_text_hash(self, file_info : FileInfo) -> int:
        """Extract percentual simhash from pdf file. 
        From text, if it is possible, if not, count image pahsh."""
        path = file_info.get_path()
        with suppress_stderr():
            try:
                text = self._extract_text_fom_pdf(path)
                return self.extract_hash_from_text(text)
            except Exception as e:
                return self._unhashable_file_exception(file_info, e)

    def extract_image_hash(self, file_info : FileInfo) -> int:
        """Extract phash from images of pdf, if it is possible."""
        if file_info.get_text_hash():
            return None
        path = file_info.get_path()
        with suppress_stderr():
            try:
                phash = 0
                with fitz.open(path) as pdf:
                    for i, page in enumerate(pdf):
                        if i >= PDF_IMAGE_MAX_PAGES:
                            file_info.set_auto_removability(False)
                            break        
                        pix = page.get_pixmap(dpi=150)
                        img = Image.open(io.BytesIO(pix.tobytes()))
                        phash ^= self.get_phash_value(img)
                return phash
            except Exception as e:
                return self._unhashable_file_exception(file_info, e)

    def _extract_text_fom_pdf(self, path : Path) -> int:
        """Extract text from PDF file."""
        text = ''
        with fitz.open(path) as pdf:
            for page in pdf:
                extracted = page.get_text()
                if extracted:
                    text += extracted + '\n'
        return text

    def _unhashable_file_exception(self, file_info : FileInfo, error : Exception) -> int:
        """Return true, if specified file is unsupported type .ppt."""
        self.logger.add_to_corrupted(file_info, error)
        return None
