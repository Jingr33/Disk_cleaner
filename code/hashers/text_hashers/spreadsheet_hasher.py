import pandas as pd

from file_data.file_info import FileInfo
from hashers.text_hashers.text_hasher_base import TextHasherBase

class SpreadsheetHasher(TextHasherBase):
    def __init__(self, sorter, logger):
        super().__init__(sorter, logger)

    def _extract_text(self, file_info : FileInfo) -> str:
        """Extract spreadsheet file, return content as a string."""
        try:
            path = file_info.get_path()
            df = None
            if path.suffix.lower() == '.csv':
                df = pd.read_csv(path)
            else:
                df = pd.read_excel(path, engine='openpyxl')
            df_text = df.to_csv(index=False)
            return df_text
        except Exception as e:
            self.logger.add_to_corrupted(file_info, e)
            return None
