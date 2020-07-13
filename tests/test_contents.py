import pytest

from swr_ed import ALL_MANAGERS
from swr_ed.base import SWRDataManager


@pytest.mark.parametrize("manager_cls", ALL_MANAGERS)
def test_contents(manager_cls, snapshot):
    if issubclass(manager_cls, SWRDataManager):
        manager = manager_cls(fetch_names=True)
    else:
        manager = manager_cls()
    manager.load()
    if manager.md5_checksum == manager.expected_md5_checksum:
        snapshot.assert_match(manager.data)
