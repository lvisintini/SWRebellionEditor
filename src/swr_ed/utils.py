import os

from . import ALL_MANAGERS


def list_unprocessed_files():
    processed_files = [c.filename for c in ALL_MANAGERS]
    data_path = os.path.join(os.getenv('SW_REBELLION_DIR'), 'GDATA')
    all_data_files = set([filename for filename in os.listdir(data_path) if filename.endswith('.DAT')])
    return [filename for filename in all_data_files.difference(processed_files)]
