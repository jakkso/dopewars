"""
Contains tests for player class
"""

from pytest import raises

from dopewars.drugs import Drug, InventoryDrug
from dopewars.player import Player
from dopewars.weapons import Blackmail, Gun, Knife


def test_player_creation() -> None:
    """
    Tests player creation
    """
    p = Player("Bob", 5000)
    assert p.money == 5000
    assert str(p) == "Bob: 5000"
    assert p.inv == {}


def test_player_buying_drug() -> None:
    """
    Tests player buying a drug
    """
    p = Player("Bob", 5000)
    soma = Drug("Soma", 100, 12)
    orig_quantity = soma.quantity
    p.buy_drugs(soma, 5)
    assert soma.quantity == orig_quantity - 5
    p.inv = {"Soma": InventoryDrug("Soma", 5)}
    p.buy_drugs(soma, 1)
    assert soma.quantity == orig_quantity - 6
    p.inv = {"Soma": InventoryDrug("Soma", 6)}
    with raises(RuntimeError):
        p.buy_drugs(soma, 50000)
        assert soma.quantity == orig_quantity - 6
        p._money = 0
        p.buy_drugs(soma, 1)
        assert soma.quantity == orig_quantity - 6


def test_player_selling_drug() -> None:
    """
    Tests that money increases and inv decreases when player sells drug
    """
    p = Player("Bob", 5000)
    with raises(RuntimeError):
        p.sell("Soma", 5, 5)
        p.sell("Soma", -5, 5)
        p.sell("Coffee", 2, 5)
    p.inv = {"Soma": InventoryDrug("Soma", 10)}
    with raises(RuntimeError):
        p.sell("Soma", 11, 5)
    p.sell("Soma", 5, 5)
    assert p.money == 5025
    assert p.inv["Soma"].quantity == 5
    p.sell("Soma", 5, 5)
    assert p.money == 5050
    assert p.inv.get("Soma") is None


def test_player_steal_money() -> None:
    """
    Tests stealing from player
    """
    p = Player("Bob", 5000)
    stolen = p.steal_money()
    assert p.money < 5000
    assert isinstance(stolen, str)


def test_player_steal_drugs() -> None:
    """
    Tests stealing drug method.
    :return:
    """
    p = Player("Bob", 5000)
    nothing = p.steal_drugs()
    assert nothing == "Nothing to take!"
    p.inv = {"Soma": InventoryDrug("Soma", 10)}
    p.steal_drugs()
    assert p.inv["Soma"].quantity < 10


def test_player_setter() -> None:
    """
    Testing that the setter method works correctly
    """
    p = Player('', 500)
    p.money += 100
    assert p.money == 600


def test_set_weapon() -> None:
    """
    :return:
    """
    bob = Player('Bob', 5000)
    gun = Gun()
    bob.weapon = gun
    assert bob.weapon == Gun()
    assert bob.money == 4500
    with raises(RuntimeError):
        bob.weapon = Blackmail()
    bob.money = 1_000_000
    bob.weapon = Blackmail()
    assert bob.weapon == Blackmail()

