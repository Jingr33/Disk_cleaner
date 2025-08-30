from tqdm import tqdm
from rapidfuzz import fuzz

from hashers.text_hashers.text_hasher import TextHasher
from hashers.text_hashers.docx_hasher import DocxHasher
from hashers.combined_hashers.pdf_hasher import PdfHasher
from hashers.phash_hashers.image_hasher import ImageHasher
from hashers.text_hashers.spreadsheet_hasher import SpreadsheetHasher
from hashers.combined_hashers.presentation_hasher import PresentationHasher
from hashers.text_hashers.html_hasher import HtmlHasher
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
        by_hash_sorted_files = {}
        for file_type, one_type_files in sorted_files.items():
            for file_info in tqdm(one_type_files, desc=hashing_info['hashing'](file_type.name), unit='file'):
                hashers[file_type].extract_hashes(file_info)
            by_hash_sorted_files[file_type] = self._sorter.sort_by_hash(file_type, one_type_files)

        hashing_info['end']()
        self._logger.log_corrupted_files()
        return by_hash_sorted_files
        
    def sequence_matcher(hash1: str, hash2: str) -> float:
        """Count percentual similarity of two files."""
        if hash1 == hash2:
            return 1
        return 0

    def hamming_similarity_simhash(simhash1 : int, simhash2 : int, bits = 128) -> float:
        """Return percentage similarity of two simhashes."""
        if not simhash1 or not simhash2:
            return 0.0
        hamming_distance = bin(simhash1 ^ simhash2).count('1')
        similarity = (1 - hamming_distance / bits)
        return round(similarity, 2)

    def hamming_distance_images(hash1 : int, hash2 : int) -> float:
        """Return percentage similarity of two image hashes."""
        if not hash1 or not hash2:
            return 0.0
        xored = hash1 ^ hash2
        hamming_distance = bin(xored).count("1")
        similarity = 1 - (hamming_distance / 64)
        return round(similarity, 2)

    def levenshtein_text_similarity(text1 : str, text2 : str) -> float:
        """Return similarity counted as a Levenshtein similarity hash."""
        return fuzz.ratio(text1, text2) / 100