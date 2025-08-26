import pandas as pd

from file_data.file_info import FileInfo
from hashers.text_hasher import TextHasher

class SpreadsheetHasher(TextHasher):
    def __init__(self, sorter, logger):
        super().__init__(sorter, logger)

    def extract_hash(self, file_info : FileInfo) -> str:
        """Extract spreadsheet file, return content as a string."""
        try:
            path = file_info.get_path()
            df = None
            if path.suffix.lower() == '.csv':
                df = pd.read_csv(path)
            else:
                df = pd.read_excel(path, engine='openpyxl')
            df_text = df.to_csv(index=False)
            return self.extract_hash_from_text(df_text)
        except Exception as e:
            self.logger.add_to_corrupted(file_info, e)
            return None
