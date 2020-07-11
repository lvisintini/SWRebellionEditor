import os

from . import ALL_MANAGERS
from .base import SWRDataManager


def list_unprocessed_files():
    processed_files = [c.filename for c in ALL_MANAGERS]
    data_path = os.path.join(os.getenv('SW_REBELLION_DIR'), 'GDATA')
    all_data_files = set([filename for filename in os.listdir(data_path) if filename.endswith('.DAT')])
    return [filename for filename in all_data_files.difference(processed_files)]


def print_csv(manager_class):
    if issubclass(manager_class, SWRDataManager):
        manager = manager_class(fetch_names=True)
        manager.load_file()
        print('"' + '","'.join(manager.data_fields_structure.keys()) + '"')
        for row in manager.data:
            print('"' + '","'.join([str(v) for v in row.values()]) + '"')
    else:
        manager = manager_class()
        manager.load_file()
        for row in manager.data:
            print('"' + '","'.join([str(v) for v in row]) + '"')
