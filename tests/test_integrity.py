import hashlib

import pytest

from swr_ed.base import ALL_MANAGERS


@pytest.mark.parametrize("manager_cls", ALL_MANAGERS)
def test_stream_integrity(manager_cls):
    manager = manager_cls()
    manager.loaded_md5_checksum()
    loaded_stream = manager.load_file()

    manager.load()

    composed_stream = manager.prepare_output_stream()
    composed_checksum = hashlib.md5(loaded_stream.read()).hexdigest()

    assert composed_stream == composed_checksum
