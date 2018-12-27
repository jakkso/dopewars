"""
Contains implementation of a Day
"""

from typing import List

from dopewars.drugs import Drug


class Day:
    """
    Day represents a single turn of the game.  Player can make trades, possibly
    encounter random events and will end the turn by traveling to another city
    """
    def __init__(self, city: str, player) -> None:
        self.city = city
        self._player = player
        self._drugs = None
        self._cops()
        self._robbers()
        self._equipment()

    def __str__(self):
        return f'City {self.city}'

