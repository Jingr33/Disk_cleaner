from tqdm import tqdm

from file_data.file_info import FileInfo
from console_writer import ConsoleWriter

class DuplicityNamesRemover():
    def __init__(self, sorted_file_infos : dict) -> None:
        self._all_duplicities = {}
        self._find_same_names_files(sorted_file_infos)
        self._remove_duplicate_name_files()

    def _find_same_names_files(self, sorted_file_infos: dict) -> None:
        """Find all pairs of files with identical names."""
        with tqdm(total=len(sorted_file_infos.keys()), desc=ConsoleWriter.detect_same_name_files(), unit='file type') as pbar:
            for _, file_infos in sorted_file_infos.items():
                if len(file_infos) <= 1:
                    pbar.update(1)
                    continue
                names = {}
                for file_info in file_infos:
                    file_name = file_info.get_name()
                    names.setdefault(file_name, []).append(file_info)
                    self._all_duplicities |= {key: value for key, value in names.items() if len(value) > 1}
                pbar.update(1)
        ConsoleWriter.same_name_files_count(len(self._all_duplicities.keys()))

    def _remove_duplicate_name_files(self) -> None:
        remove_all_automaticly = False
        keys = list(self._all_duplicities.keys())
        for i in range(len(keys), -1, -1):
            name = keys[i - 1]
            user_input = 'n'
            ConsoleWriter.duplicity_file_name_detected(self._all_duplicities[name])
            if not remove_all_automaticly:
                user_input = ConsoleWriter.ask_remove_duplicity_name_files()

            if user_input == 'All' or remove_all_automaticly:
                self._all_duplicities[0] = self._remove_duplicate_name_file(self._all_duplicities[name])
                remove_all_automaticly = True
            elif user_input == 'Y':
                self._all_duplicities[0] = self._remove_duplicate_name_file(self._all_duplicities[name])
            else:
                ConsoleWriter.file_saved(self._all_duplicities[name][0])
        ConsoleWriter.duplicity_names_removing_completed()

    def _remove_duplicate_name_file(self, duplicities : list[FileInfo]) -> list[FileInfo]:
        while len(duplicities) >= 2:
            file_info = duplicities.pop(-1)
            file_info.get_path().unlink()
            ConsoleWriter.file_deleted(file_info, True)
        return duplicities
