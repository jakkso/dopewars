"""
Contains tests for scores class
"""

from dopewars.scores import Scores


def test_add_score() -> None:
    """
    Test for adding new score to Scores
    """
    s = Scores("")
    s.list = [(100, "al"), (99, "bob"), (101, "charlie"), (105, "dave"), (55, "eric")]
    s._sort()
    assert s.list == [
        (105, "dave"),
        (101, "charlie"),
        (100, "al"),
        (99, "bob"),
        (55, "eric"),
    ]

    frank = (44, "frank")
    s.add(frank)
    assert s.list == [
        (105, "dave"),
        (101, "charlie"),
        (100, "al"),
        (99, "bob"),
        (55, "eric"),
    ]
    frank = (56, "frank")
    s.add(frank)
    assert s.list == [
        (105, "dave"),
        (101, "charlie"),
        (100, "al"),
        (99, "bob"),
        (56, "frank"),
    ]
    greg = (106, "greg")
    s.add(greg)
    assert s.list == [
        (106, "greg"),
        (105, "dave"),
        (101, "charlie"),
        (100, "al"),
        (99, "bob"),
    ]
