from pathlib import Path

from config import FILE_TYPES

class Sorter():
    def __init__(self, unsorted_files : list[Path]):
        self.unsorted_files = unsorted_files
        self.sorted_files = {}

    def sort_by_extension(self) -> dict:
        """Sort files into groups by file type."""
        self.sorted_files = {}
        for type in FILE_TYPES:
            self.sorted_files[type] = []

        for file_path in self.unsorted_files:
            file_extension = file_path.suffix
            if file_extension in ['.txt', '.md']:
                self.sorted_files['text'].append(file_path)
            elif file_extension == '.docx':
                self.sorted_files['docx'].append(file_path)
            elif file_extension in ['.doc', '.docm']:
                self.sorted_files['doc'].append(file_path)
            elif file_extension == '.pdf':
                self.sorted_files['pdf'].append(file_path)
            elif file_extension in ['.ppt', '.pptx']:
                self.sorted_files['pptx'].append(file_path)
            elif file_extension in ['.csv', '.xlsx', '.xls']:
                self.sorted_files["spreadsheet"].append(file_path)
            elif file_extension.lower() in ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tif', '.heic']:
                self.sorted_files['image'].append(file_path)
            elif file_extension == '.htm':
                self.sorted_files['htm'].append(file_path)
            else:
                self.sorted_files['other'].append(file_path)
        return self.sorted_files
