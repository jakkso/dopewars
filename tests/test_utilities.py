"""
Gameplay tests
"""
from dopewars.utilities import fmt_money


def test_format_money() -> None:
    """
    Test for format money
    :return:
    """
    assert fmt_money(1) == "$1"
    assert fmt_money(100) == "$100"
    assert fmt_money(1000) == "$1,000"
    assert fmt_money(100000) == "$100,000"
    assert fmt_money(1000000) == "$1,000,000"
    assert "$10,000,000" == fmt_money(10000000)
