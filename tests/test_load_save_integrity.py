import hashlib

import pytest

from swr_ed.base import ALL_MANAGERS


@pytest.mark.parametrize("manager_cls", ALL_MANAGERS)
def test_load_save_integrity(manager_cls, snapshot):
    manager = manager_cls()
    manager.load_file()
    stream = manager.prepare_file()
    assert manager.loaded_md5_checksum == hashlib.md5(stream.read()).hexdigest()
