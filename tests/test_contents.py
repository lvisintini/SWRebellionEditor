import pytest

from swr_ed.base import ALL_MANAGERS


@pytest.mark.parametrize("manager_cls", ALL_MANAGERS)
def test_contents(manager_cls, snapshot):
    manager = manager_cls()
    manager.load_file()
    snapshot.assert_match(manager.data_dicts)


def test_lalal(snapshot):
    manager = ALL_MANAGERS[0]()
    manager.load_file()
    snapshot.assert_match(manager.data_dicts)