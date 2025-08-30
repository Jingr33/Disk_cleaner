from enum import Enum

class SimThreshold(Enum):
    SIMHASH_MIN = 0,
    LEVENSHTEIN_MIN = 1,
    PHASH_MIN = 2,
    AUTO_REMOVE = 3,