"""
Contains tests for player class
"""

from pytest import raises

from dopewars.drugs import Drug, InventoryDrug
from dopewars.player import Player


def test_player_creation() -> None:
    """
    Tests player creation
    """
    p = Player('Bob', 5000)
    assert p.money == 5000
    assert str(p) == 'Bob: 5000'
    assert p.inv == {}


def test_player_buying_drug() -> None:
    """
    Tests player buying a drug
    """
    p = Player('Bob', 5000)
    soma = Drug('Soma', 100, 12)
    orig_quantity = soma.quantity
    p.buy(soma, 5)
    assert soma.quantity == orig_quantity - 5
    p.inv = {'Soma': InventoryDrug('Soma', 5)}
    p.buy(soma, 1)
    assert soma.quantity == orig_quantity - 6
    p.inv = {'Soma': InventoryDrug('Soma', 6)}
    with raises(RuntimeError):
        p.buy(soma, 50000)
        assert soma.quantity == orig_quantity - 6
        p._money = 0
        p.buy(soma, 1)
        assert soma.quantity == orig_quantity - 6

