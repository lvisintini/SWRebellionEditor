import hashlib

import pytest

from swr_ed.base import ALL_MANAGERS


@pytest.mark.parametrize("manager_cls", ALL_MANAGERS)
def test_stream_integrity(manager_cls):
    manager = manager_cls()
    manager.load()

    loaded_checksum = manager.md5_checksum

    composed_stream = manager.prepare_output_stream()
    composed_checksum = hashlib.md5(composed_stream.read()).hexdigest()

    assert loaded_checksum == composed_checksum
