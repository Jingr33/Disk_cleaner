from pathlib import Path
from PIL import Image
import docx
import PyPDF2
from PyPDF2.errors import PdfReadError
import pandas as pd
import imagehash
import win32com.client
import pptx
import hashlib
from bs4 import BeautifulSoup
from zipfile import is_zipfile
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from tqdm import tqdm

from logger import Logger
from console_writer import ConsoleWriter
from decorators import suppress_stderr

class Hasher():
    def __init__(self, logger : Logger):
        self.logger = logger

    def count_hashes(self, sorted_files : dict) -> dict:
        """Count percentual hash of all files in inpued dict, 
        return dict with added hash to each file"""
        hashed_files = {file_type: [] for file_type in sorted_files}
        
        hash_functions = {
            "text" : self.extract_text_file,
            "docx" : self.extract_docx_file,
            "doc" : self.extract_doc_file,
            "pdf" : self.extract_pdf_file,
            "spreadsheet" : self.extract_spreadsheet_file,
            "pptx" : self.extract_ppt_file,
            "htm" : self.extract_htm_file,
            "image" : self.get_image_phash,
        }

        hashing_info = ConsoleWriter.get_hash_counting_info()

        hashing_info['start']()
        for file_type, files in sorted_files.items():
            for file_path in tqdm(files, desc=hashing_info['hashing'](file_type), unit="file"):
                file_hash = hash_functions[file_type](file_path)
                hashed_files[file_type].append((file_path, file_hash))

        hashing_info['end']()
        return hashed_files

    def extract_text_file(self, path: Path) -> str:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    def is_probably_valid_docx(path: Path) -> bool:
        return path.suffix.lower() == ".docx" and is_zipfile(path)
        
    def extract_doc_file(self, path: Path) -> str:
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

    def extract_docx_file(self, path: Path) -> str:
        try:
            if Hasher.is_probably_valid_docx(path):
                doc = docx.Document(path)
                return "\n".join([para.text for para in doc.paragraphs])
            else:
                return None
        except Exception as e:
            self.logger.add_to_corrupted(path)
            return None

    def _read_pdf(path: Path) -> str:
        text = ""
        with open(path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
        return text

    def extract_pdf_file(self, path: Path) -> str:
        with suppress_stderr():
            try:
                with ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(Hasher._read_pdf, path)
                    return future.result(timeout=4)    
            except TimeoutError:
                self.logger.add_to_corrupted(path)
                return None
            except PdfReadError as e:
                self.logger.add_to_corrupted(path)
                return None
            except Exception as e:
                self.logger.add_to_corrupted(path)
                return None

    def extract_spreadsheet_file(self, path: Path) -> str:
        try:
            if path.suffix.lower() == ".csv":
                df = pd.read_csv(path)
            else:
                df = pd.read_excel(path, engine='openpyxl')
            return df.to_csv(index=False)
        except:
            self.logger.add_to_corrupted(path)
            return None
        
    def extract_ppt_file(self, path: Path) -> str:
        try:
            prs = pptx.Presentation(path)
            text_runs = []
            for slide in prs.slides:
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        text_runs.append(shape.text)
            return "\n".join(text_runs)
        except Exception as e:
            self.logger.add_to_corrupted(path)
            return f"ERROR: {e}"

    def extract_htm_file(self, path: Path) -> str:
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                soup = BeautifulSoup(f, "html.parser")
            return soup.get_text()
        except Exception as e:
            self.logger.add_to_corrupted(path)
            return f"ERROR: {e}"

    def get_image_phash(self, path: Path):
        try:
            hash = imagehash.average_hash(Image.open(path))
            return str(hash)
        except Exception as e:
            self.logger.add_to_corrupted(path)
            return None
