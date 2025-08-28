from pathlib import Path

from file_data.file_type_enum import FileType

class FileInfo():
    def __init__(self, path : Path):
        self._path = path
        self._suffix = self._path.suffix
        self._type = None
        self._text_hash = None
        self._image_hash = None
        self.auto_removable = True
        self._error = None
        self._restore_path = None
        self.set_type()

    def set_type(self) -> None:
        """Set a type of the file."""
        if self._suffix in ['.txt', '.md']:
            self._type = FileType.TEXT
        elif self._suffix == '.docx':
            self._type = FileType.DOCX
        elif self._suffix in ['.doc', '.docm']:
            self._type = FileType.DOC
        elif self._suffix == '.pdf':
            self._type = FileType.PDF
        elif self._suffix in ['.ppt', '.pptx']:
            self._type = FileType.PRESENTATION
        elif self._suffix in ['.csv', '.xlsx', '.xls']:
            self._type = FileType.SPREADSHEET
        elif self._suffix.lower() in ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tif', '.heic']:
            self._type = FileType.IMAGE
        elif self._suffix in ['.htm', '.html']:
            self._type = FileType.HTML
        else:
            self._type = FileType.OTHER

    def set_new_path(self, path : Path) -> None:
        """Set path of the file."""
        self._path = path

    def set_text_hash(self, text_hash : int) -> None:
        """Set percentual hash counted from text of the file."""
        self._text_hash = text_hash

    def set_image_hash(self, image_hash : int) -> None:
        """Set percentual hash counted from images in the file."""
        self._image_hash = image_hash

    def set_auto_removability(self, is_auto_removable : bool) -> None:
        """Set auto_removable property."""
        self.auto_removable = is_auto_removable

    def set_error(self, error : str) -> None:
        """Set error of the file."""
        self._error = error

    def set_restore_path(self) -> None:
        """Set _restore_path for restore from bin."""
        self._restore_path = self._path

    def get_path(self) -> Path:
        """Return path of the file."""
        return self._path

    def get_name(self) -> str:
        """Return name of the file."""
        return self._path.name

    def get_type(self) -> FileType:
        """Return one of supported file type or type 'other'."""
        return self._type

    def get_suffix(self) -> str:
        """Return suffix of the file
        (example: '.txt')"""
        return self._path.suffix

    def get_text_hash(self) -> int:
        """Return a text hash of the file."""
        if self._text_hash:
            return self._text_hash
        return None

    def get_image_hash(self) -> int:
        """Return an image hash of the file."""
        if self._image_hash:
            return self._image_hash
        return None

    def get_combined_hash(self) -> int:
        """Return combined hash of the file."""
        combined_hash = 0
        if self._text_hash:
            combined_hash += self._text_hash
        if self._image_hash:
            combined_hash += self._image_hash
        return combined_hash

    def get_folder(self) -> Path:
        """Return a folder of the file."""
        return self._path.parent

    def get_error_or_default(self) -> str:
        """Return error of the file or default."""
        return self._error

    def get_restore_path(self) -> Path:
        """Return restore path of the file."""
        return self._restore_path

    def is_auto_removable(self) -> bool:
        """Return, if file is automatically removable."""
        return self.auto_removable