import pytest

from swr_ed.base import ALL_MANAGERS


@pytest.mark.parametrize("manager_cls", ALL_MANAGERS)
def test_load_save_integrity(manager_cls, snapshot):
    manager = manager_cls()
    manager.load_file()
    original_checksum = manager.loaded_md5_checksum

    manager.save_file()

    manager = manager_cls()
    manager.load_file()

    assert original_checksum == manager.loaded_md5_checksum
