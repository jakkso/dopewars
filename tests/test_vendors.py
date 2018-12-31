"""
Contains tests for vendors
"""


from dopewars.banks import *


def test_deposit_withdraw() -> None:
    """
    Checks that deposit / withdraw / balance work correctly
    """
    b = Bank("", 0.05)
    msg = b.deposit(100)
    assert msg == "Balance: $100"
    assert b.balance == 100
    cash = b.withdraw(101)
    assert cash == 0
    cash = b.withdraw(50)
    assert cash == 50
    assert b.balance == 50


def test_initial_deposit() -> None:
    """
    Tests a bank variation requires a minimum initial deposit.
    After the initial deposit, no min is required to deposit funds,
    even if all were removed.
    """
    b = Bank("", 0.10, 50000)
    msg = b.deposit(10000)
    assert msg == "Amount must be greater than $50,000"
    msg = b.deposit(50000)
    assert msg == "Balance: $50,000"
    cash = b.withdraw(50000)
    assert cash == 50000
    msg = b.deposit(100)
    assert msg == "Balance: $100"


def test_calc_interest() -> None:
    """
    Checks that the interest calculator works as expected
    """
    b = Bank("", 0.05)
    b.deposit(100)
    b.calc_interest()
    assert b.balance == 105


def test_texas_midland_goldman() -> None:
    """
    Test Texas Midland's & Goldman Sacks
    """
    t = TexasMidland()
    msg = t.deposit(1000)
    assert msg == "Balance: $1,000"
    g = GoldmanSacks()
    msg = g.deposit(100_000)
    assert msg == "Amount must be greater than $1,000,000"
    msg = g.deposit(1_000_000)
    for _ in range(2):
        g.calc_interest()
    assert g.balance > 1_000_000
    print(g.balance)
