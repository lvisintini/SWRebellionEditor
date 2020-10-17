import os
from abc import ABC, abstractmethod


class DLLBaseWrapper(ABC):

    @property
    @abstractmethod
    def relative_path(self):
        raise NotImplemented()

    @property
    @abstractmethod
    def library(self):
        raise NotImplemented()

    def __init__(self, data_path: str = None):
        self.data_path = data_path or os.getenv('SW_REBELLION_DIR')
        self.file_path = os.path.join(self.data_path, self.relative_path)
