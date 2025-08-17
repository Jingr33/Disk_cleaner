import pptx

from file_data.file_info import FileInfo
from hashers.hasher_base import HasherBase

class PresentationHasher(HasherBase):
    def __init__(self, sorter, logger):
        super().__init__(sorter, logger)

    def extract_hash(self, file_info : FileInfo) -> str:
        """Extract ppt file (presentation), return content as a string."""
        path = file_info.get_path()
        try:
            prs = pptx.Presentation(path)
            text_runs = []
            for slide in prs.slides:
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        text_runs.append(shape.text)
            # return "\n".join(text_runs)
            return None
        except Exception as e:
            self.logger.add_to_corrupted(path)
            return f"ERROR: {e}"
