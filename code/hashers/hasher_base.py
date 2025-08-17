from sorter import Sorter
from logger import Logger

class HasherBase():
    def __init__(self, sorter : Sorter, logger : Logger):
        self._sorter = sorter
        self.logger = logger
