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
        self.inv: dict[str: InventoryDrug] = {}

    def buy(self, drug: Drug, quantity: int):
        """
        :param quantity:
        :param drug:
        :return:
        """
        if quantity > drug.quantity:
            return 1
        price = quantity * drug.price
        if self._money < price:
            return 2
        purchase = InventoryDrug(drug.name, quantity)
        drug.quantity -= quantity
        if self.inv.get(drug.name) is None:
            self.inv[drug.name] = purchase
        else:
            self.inv[drug.name] += purchase









