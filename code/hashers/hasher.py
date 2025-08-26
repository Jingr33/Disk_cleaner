from tqdm import tqdm

from hashers.text_hasher import TextHasher
from hashers.docx_hasher import DocxHasher
from hashers.pdf_hasher import PdfHasher
from hashers.image_hasher import ImageHasher
from hashers.spreadsheet_hasher import SpreadsheetHasher
from hashers.presentation_hasher import PresentationHasher
from hashers.html_hasher import HtmlHasher
from hashers.other_hasher import OtherHasher
from file_data.file_type_enum import FileType
from console_writer import ConsoleWriter

class Hasher():
    def __init__(self, sorter, logger):
        self._sorter = sorter
        self._logger = logger

    def count_hashes(self, sorted_files : dict) -> None:
        """Count percentual hash of all files in inpued dict, 
        set hash in each FileData object."""   
        hashers = {
            FileType.TEXT : TextHasher(self._sorter, self._logger),
            FileType.DOCX : DocxHasher(self._sorter, self._logger),
            FileType.DOC : DocxHasher(self._sorter, self._logger),
            FileType.PDF : PdfHasher(self._sorter, self._logger),
            FileType.SPREADSHEET : SpreadsheetHasher(self._sorter, self._logger),
            FileType.PRESENTATION : PresentationHasher(self._sorter, self._logger),
            FileType.HTML : HtmlHasher(self._sorter, self._logger),
            FileType.IMAGE : ImageHasher(self._sorter, self._logger),
            FileType.OTHER : OtherHasher(self._sorter, self._logger),
        }

        hashing_info = ConsoleWriter.get_hash_counting_info()

        hashing_info['start']()
        for file_type, one_type_files in sorted_files.items():
            for file_info in tqdm(one_type_files, desc=hashing_info['hashing'](file_type.name), unit='file'):
                file_info.set_hash(hashers[file_type].extract_hash(file_info))
            one_type_files = self._sorter.sort_by_hash(one_type_files)

        hashing_info['end']()
        self._logger.log_corrupted_files()
        return sorted_files
        
    def _sequence_matcher(hash1: str, hash2: str) -> float:
        """Count percentual similarity of two files."""
        if hash1 == hash2:
            return 1
        return 0

    def _hamming_similarity_simhash(simhash1 : int, simhash2 : int) -> float:
        """Return percentage similarity of two simhashes."""
        hamming_distance = bin(simhash1 ^ simhash2).count('1')
        similarity = (1 - hamming_distance / 64)
        return round(similarity, 2)

    def _hamming_distance_images(hash1 : int, hash2 : int) -> int:
        """Return percentage similarity of two image hashes."""
        hamming_distance = abs(hash1 - hash2)
        similarity = (1 - hamming_distance / 64)
        return round(similarity, 2)

    def similarity_score(hash1, hash2, file_type) -> float:
        """Return similarity score (percentage) of two hashes."""
        if not hash1 or not hash2:
            return 0
        if file_type in ['text', 'doc', 'docx', 'pdf']:
            return Hasher._hamming_similarity_simhash(hash1, hash2)
        elif file_type == 'image':
            return Hasher._hamming_distance_images(hash1, hash2)
        else:
            return Hasher._sequence_matcher(str(hash1), str(hash2))
