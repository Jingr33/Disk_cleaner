from pathlib import Path
import pandas as pd

from hashers.text_hasher import TextHasher

class SpreadsheetHasher(TextHasher):
    def __init__(self, sorter, logger):
        super().__init__(sorter, logger)

    def extract_hash(self, path: Path) -> str:
        """Extract spreadsheet file, return content as a string."""
        try:
            df = None
            if path.suffix.lower() == ".csv":
                df = pd.read_csv(path)
            else:
                df = pd.read_excel(path, engine='openpyxl')
            df_text = df.to_csv(index=False)
            return self.extract_hash_from_text(df_text)
        except:
            self.logger.add_to_corrupted(path)
            return None
