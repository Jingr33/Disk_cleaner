from removers.remover_base import RemoverBase
from hashers.hasher import Hasher
from backuper.backuper import Backuper
from file_data.file_info import FileInfo
from removers.type_simliarity_thresholds import SIM_THRESHOLDS
from removers.similarity_threshold_keys_enum import SimThreshold
from hashers.hash_type_enum import HashType

class ByImageRemover(RemoverBase):
    def __init__(self, file_infos : list[FileInfo], backuper : Backuper) -> None:
        super().__init__(file_infos, backuper)

    def hash_based_pruning_of_type(self, file_infos : list[FileInfo]) -> None:
        """Compare neighbour hashes in file_infos list (by image hashes).
        Manage remove depending on hash similarity."""
        image_sorted_file_infos = file_infos[HashType.IMAGE]
        super().hash_based_pruning_of_type(image_sorted_file_infos)

    def _compare_two_files(self, file_infos : list[FileInfo], fi1_idx : int) -> None:
        """Compare file similarity with all remaining files (by image hash).
        Remove one of files or not depending on hash simiarity."""
        fi2_idx = fi1_idx - 1
        file_info1 = file_infos[fi2_idx]
        file_info2 = file_infos[fi1_idx]
        sim_score = Hasher.hamming_distance_images(file_info2.get_image_hash(), file_info1.get_image_hash())
        print(sim_score)
        if sim_score >= SIM_THRESHOLDS[file_info1.get_type()][SimThreshold.PHASH_MIN]:
            self._manage_remove(sim_score, file_infos, fi1_idx, fi2_idx)
