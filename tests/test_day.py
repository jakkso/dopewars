"""
Contains tests for Day
"""
from pytest import raises

from dopewars.day import Day
from dopewars.drugs import Drug, InventoryDrug
from dopewars.player import Player
from dopewars.drugs import Weed
from dopewars.weapons import Blackmail, Knife, Gun


def test_day_init() -> None:
    """
    Tests that day initializes properly
    """
    p = Player("bob", 5000)
    nyc = Day("NYC", p)
    assert len(nyc._drugs) == 8
    for _, drug in nyc._drugs.items():
        assert isinstance(drug, Drug)


def test_day_buy() -> None:
    """
    Tests that player can successfully buy drugs.
    """
    bob = Player("Bob", 1)
    day = Day("Miami!", bob)
    weed = Weed()
    weed.quantity = 1
    day._drugs["Weed"] = weed
    with raises(RuntimeError):
        day.buy(
            "Weed", 0
        )  # Trying to buy nothing or nonsensical amount raises a RuntimeError
        day.buy("Weed", -5000)
        day.buy("Weed", 1)  # Same as when you have insufficient funds
    day.player._money = 5000  # Too bad this doesn't work IRL
    orig_quantity = day._drugs["Weed"].quantity
    day.buy("Weed", 1)
    assert day.player.inv["Weed"].quantity == 1
    assert day._drugs["Weed"].quantity + 1 == orig_quantity
    with raises(RuntimeError):
        day.buy("Weed", 1)


def test_day_sell() -> None:
    """
    Tests that play can sell drugs
    """
    bob = Player("Bob", 500)
    bob.inv["Weed"] = InventoryDrug("Weed", 1)
    day = Day("Miami", bob)
    day.player = (
        bob
    )  # Events happen randomly, this prevents an event from unexpectedly lowering the player's money
    day.sell("Weed", 1)
    assert day.player.money > 500
    assert day.player.inv == {}


def test_day_event_freq() -> None:
    """
    Tests Day._event frequency
    :return:
    """
    p = Player("Bob", 100000)
    events = []
    for _ in range(500):
        d = Day("test", p)
        if d.event_text:
            events.append(1)
    assert len(events) > 10


def test_weaponry_usage() -> None:
    """
    Tests
    :return:
    """
