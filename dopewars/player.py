"""
Contains Player definition
"""
from typing import List

from dopewars.drugs import Drug, InventoryDrug


class Player:
    """
    Defines how the player works, contains money and inventory
    """
    def __init__(self, name: str, money: int) -> None:
        """

        """
        self.name = name
        self._money = money
        self.inv: List[InventoryDrug] = []







