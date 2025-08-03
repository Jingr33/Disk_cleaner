import os
from pathlib import Path
import argparse
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from remover import Remover
from sorter import Sorter
from logger import Logger
from hasher import Hasher
from console_writer import ConsoleWriter
from config import *

class Cleaner():
    def __init__(self, args):
        self.root = self._set_disk_root(args.root)
        self.total_files = 0
        self.all_files = self._explore_disk(ROOT_FOLDER, [], True)
        self.sorted_files = {}
        self.files_with_hashes = {}
        self._remover = Remover(self.all_files, args.minsim, args.autosim)
        self._sorter = Sorter(self.all_files)
        self._logger = Logger()
        self._hasher = Hasher(self._logger)
        self._prepare_for_cleaning()
        self._remove_wave_starters(args.wavers)
        self._clean_with_hash_comparer(args.clean)

    def _set_disk_root(self, root_arg : argparse.Namespace) -> str:
        """Set root folder of the disk depends on args."""
        if root_arg == "":
            return root_arg
        return ROOT_FOLDER

    def _explore_disk(self, folder_path : str, files : list[Path], 
                      print_result : bool = False) -> list[Path]:
        """Find all files inside of the root folder."""
        for item in os.listdir(folder_path):
            item_path = Path(os.path.join(folder_path, item))
            if os.path.isdir(item_path):
                files = self._explore_disk(item_path, files)
            elif item_path.exists() and item_path.is_file():
                files.append(item_path)
                self.total_files += 1
            else:
                # print corrupted file
                # TODO
                ...
            ConsoleWriter.explore_files_progress(self.total_files)

        if print_result:
            ConsoleWriter.explore_files_progress(self.total_files, False)
        return files

    def _prepare_for_cleaning(self) -> None:
        """Preparedata structures for cleaning 
        (sorted_files, file_with_hashes, pick ifles to process.)"""
        self.sorted_files = self._sorter.sort_by_extension()
        ConsoleWriter.file_counts(self.sorted_files)
        self.select_entered_file_types()
        self.files_with_hashes = self._hasher.count_hashes(self.sorted_files)
    
    def _remove_wave_starters(self, wavers_arg : argparse.Namespace) -> None:
        """Remove files with names beginning with tilda."""
        if wavers_arg:
            self.all_files = Remover.delete_wavers(self.all_files)
    
    def _clean_with_hash_comparer(self, clean_arg : argparse.Namespace):
        """Clean the disk with hash comparsion method."""
        if clean_arg:
            self._remover.hash_based_pruning(self.files_with_hashes)

    def select_entered_file_types(self) -> None:
        """Ask user for file types to pruning and remove unselected types from file dict. """
        user_input = ConsoleWriter.select_file_types_input()
        keys_to_delete = []
        for file_type in list(self.sorted_files.keys()):
            if (file_type not in user_input.lower() 
                or not self.sorted_files[file_type]):
                keys_to_delete.append(file_type)
        for key in keys_to_delete:
            del self.sorted_files[key]
