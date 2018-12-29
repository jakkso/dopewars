"""
Contains Pytest formatted tests for the drug classes
"""
from pytest import raises

from dopewars.drugs import Drug, InventoryDrug


def test_drug() -> None:
    """
    Test creation of example drug
    """
    soma = redo_surge(Drug("Soma", 100, 12), None)
    assert 112 >= soma.price >= 88  # Due to jitter, price won't be less than 100 +/- 12
    assert "Soma price: " in str(soma)
    with raises(RuntimeError):
        Drug("Soma", -1, 2)
        Drug("Soma", 12, 0)


def test_surge_drug() -> None:
    """
    Example drug, but with surges, this time.
    The values tested for change each time, but are within certain ranges
    """
    soma = redo_surge(Drug("Soma", 100, 12), "hi")
    assert 33 >= soma.quantity >= 8  #
    assert soma.price > 112
    soma = redo_surge(Drug("Soma", 100, 12), "lo")
    assert 15 <= soma.quantity <= 300
    assert soma.price <= 79  # the max price is 0.67 * 100 + 12
    assert soma.price >= 15  # the min price is 15% of base price


def test_inv_drug() -> None:
    """
    Tests creation of inv drug
    """
    soma = InventoryDrug("Soma", 22)
    assert "Soma: 22" == str(soma)


def test_inv_drug_add() -> None:
    """
    Tests InventoryDrug.__add__ method
    """
    soma = InventoryDrug("Soma", 22)
    more = InventoryDrug("Soma", 55)
    not_soma = InventoryDrug("Not Soma", 10)
    soma += not_soma
    assert soma.quantity == 22
    assert not_soma.quantity == 10
    soma += more
    assert soma.quantity == 77
    assert more.quantity == 0


def test_inv_drug_sell() -> None:
    """
    Test sell method
    """
    soma = InventoryDrug("Soma", 10)
    with raises(RuntimeError):
        too_many = soma.sell(12, 55)
        assert too_many == 0
        assert soma.quantity == 10
    sell_all = soma.sell(10, 10)
    assert sell_all == 100
    assert soma.quantity == 0
    soma = InventoryDrug("Soma", 10)
    with raises(RuntimeError):
        soma.sell(-5, 5)
        soma.sell(5, -12)
        soma + 12
        soma + "Hello there!"


def redo_surge(drug: Drug, new_surge_val) -> Drug:
    """
    Testing utility, changes surge value to new_surge_val, used to by-pass
    the random element of Drug._calc_surge
    :param drug: Drug element to be changed
    :param new_surge_val: None, 'lo' or 'hi' are valid values
    :return:
    """
    drug._surge = new_surge_val
    drug._calc_price()
    drug._calc_quantity()
    return drug
