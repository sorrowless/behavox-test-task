import pytest

from depsfinder.dataloader import DataLoader
from depsfinder.ordering import Ordering
from depsfinder.exceptions import RingDependencyError


def test_load_wrong_file():
    with pytest.raises(SystemExit):
        DataLoader().load('test')


def test_load_proper_file():
    assert DataLoader().load('fixtures/gf-test.yml') == {
        'mysql': {'deps': ['network']}, 'network': None}


def test_proper_ordering_start():
    data = DataLoader().load('fixtures/gf-test.yml')
    order = {}
    Ordering().calculateDependenciesStart(data, order)
    assert order == {'mysql': 1, 'network': 0}


def test_proper_ordering_stop():
    data = DataLoader().load('fixtures/gf-test.yml')
    order = {}
    Ordering().calculateDependenciesStop(data, order)
    assert order == {'mysql': 0, 'network': 1}


def test_cycled_ordering_start():
    data = DataLoader().load('fixtures/gf-test-wrong.yml')
    order = {}
    with pytest.raises(RingDependencyError):
        Ordering().calculateDependenciesStart(data, order)


def test_cycled_ordering_stop():
    data = DataLoader().load('fixtures/gf-test-wrong.yml')
    order = {}
    with pytest.raises(RingDependencyError):
        Ordering().calculateDependenciesStop(data, order)


def test_proper_complex_start():
    data = DataLoader().load('fixtures/bh-example.yml')
    order = {}
    Ordering().calculateDependenciesStart(data, order)
    assert order == {
        'dashboard': 4, 'elasticsearch': 0, 'fullhouse': 3, 'hadoop-namenode': 1,
        'hbase-master': 2, 'kibana': 1, 'mysql': 0, 'zookeeper': 0}


def test_proper_complex_stop():
    data = DataLoader().load('fixtures/bh-example.yml')
    order = {}
    Ordering().calculateDependenciesStop(data, order)
    assert order == {
        'dashboard': 0, 'elasticsearch': 2, 'fullhouse': 1, 'hadoop-namenode': 3,
        'hbase-master': 2, 'kibana': 0, 'mysql': 2, 'zookeeper': 4}
