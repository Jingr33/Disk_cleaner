import sys
import os
from pathlib import Path
import argparse

from file_data.file_info import FileInfo
from backuper.backuper import Backuper
from removers.remover import Remover
from sorter import Sorter
from logger import Logger
from hashers.hasher import Hasher
from console_writer import ConsoleWriter
from config import *

class Cleaner():
    def __init__(self, args) -> None:
        self.root = self._set_disk_root(args.root)
        self.total_files = 0
        self.all_file_info = self._explore_disk(ROOT_FOLDER, [], True)
        self.sorted_file_infos = {}
        self.sorted_by = {}
        self._init_dependencies()
        self._sort_files()
        self._restore_bin(args.restore_bin)
        self._remove_wave_starters(args.wavers)
        self._clean_with_hash_comparer(args.clean)
        self._remove_same_name_files(args.names)

    def _set_disk_root(self, root_arg : argparse.Namespace) -> str:
        """Set root folder of the disk depends on args."""
        root = ROOT_FOLDER
        if root_arg != '':
            root = root_arg
        if not Path(root).exists() or not Path(root).is_dir():
            ConsoleWriter.root_folder_not_found(root)
            sys.exit()
        return root

    def _init_dependencies(self) -> None:
        """Initi all dependencies."""
        self._logger = Logger()
        self._backuper = Backuper(self._logger)
        self._remover = Remover(self.all_file_info, self._backuper)
        self._sorter = Sorter(self.all_file_info)
        self._hasher = Hasher(self._sorter, self._logger)

    def _sort_files(self) -> None:
        """Sort files by file types."""
        self.sorted_file_infos = self._sorter.sort_by_file_type()
        ConsoleWriter.file_counts(self.sorted_file_infos)

    def _explore_disk(self, folder_path : str, files : list[Path], 
                      print_result : bool = False) -> list[Path]:
        """Find all files inside of the root folder."""
        for item in os.listdir(folder_path):
            item_path = Path(os.path.join(folder_path, item))
            if os.path.isdir(item_path):
                files = self._explore_disk(item_path, files)
            elif item_path.exists() and item_path.is_file():
                files.append(FileInfo(item_path))
                self.total_files += 1
            else:
                self._logger.add_to_corrupted(FileInfo(item_path), 'Failed to explore this file')
            ConsoleWriter.explore_files_progress(self.total_files)
        if print_result:
            ConsoleWriter.explore_files_progress(self.total_files, False)
        return files
 
    def _restore_bin(self, restore_bin_arg : argparse.Namespace) -> None:
        """Restore files from a disk bin."""
        if restore_bin_arg:
            self._backuper.restore_bin()
    
    def _remove_wave_starters(self, wavers_arg : argparse.Namespace) -> None:
        """Remove files with names beginning with tilda."""
        if wavers_arg:
            self.all_file_info = self._remover.delete_wavers(self.all_file_info, self._backuper)
    
    def _clean_with_hash_comparer(self, clean_arg : argparse.Namespace):
        """Clean the disk with hash comparsion method."""
        if clean_arg:
            self.select_entered_file_types()
            self.sorted_by = self._hasher.count_hashes(self.sorted_file_infos)
            self._remover.hash_based_pruning(self.sorted_by)

    def _remove_same_name_files(self, names_arg : argparse.Namespace):
        """Check eventually remove files with same names."""
        if names_arg:
            self._remover.delete_duplicity_name_files(self.sorted_file_infos)

    def select_entered_file_types(self) -> None:
        """Ask user for file types to pruning.
        Keep only selected and non-empty keys in sorted dict. """
        user_input = ConsoleWriter.select_file_types_input()
        if user_input.lower() == 'all':
            return self.sorted_file_infos
        self.sorted_file_infos = {
            key: value for key, value in self.sorted_file_infos.items()
            if key.name.lower() in user_input.lower() and value
        }