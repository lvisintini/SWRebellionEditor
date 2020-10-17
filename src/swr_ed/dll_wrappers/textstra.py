from functools import cached_property

import win32api
import pywintypes

from .base import DLLBaseWrapper


class TextStraWrapper(DLLBaseWrapper):
    relative_path = "TEXTSTRA.DLL"

    @cached_property
    def library(self):
        return win32api.LoadLibrary(self.file_path)

    def get_text(self, text_id):
        if win32api is None or pywintypes is None:
            return None
        try:
            return win32api.LoadString(self.library, text_id)
        except pywintypes.error:
            return None
