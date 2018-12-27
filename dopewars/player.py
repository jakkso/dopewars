"""
Contains Player definition
"""

from dopewars.drugs import Drug, InventoryDrug


class Player:
    """
    Defines how the player works, contains money and inventory
    """
    def __init__(self, name: str, money: int) -> None:
        self.name = name
        self._money = money
        self.inv: dict[str: InventoryDrug] = {}

    def __str__(self):
        return f'{self.name}: {self.money}'

    @property
    def money(self):
        return self._money

    def buy(self, drug: Drug, quantity: int) -> None:
        """
        :param quantity:
        :param drug:
        :return:
        """
        if quantity > drug.quantity:
            raise RuntimeError('Insufficient quantity')
        price = quantity * drug.price
        if self._money < price:
            raise RuntimeError('Insufficient funds')
        purchase = InventoryDrug(drug.name, quantity)
        drug.quantity -= quantity
        if self.inv.get(drug.name) is None:
            self.inv[drug.name] = purchase
        else:
            self.inv[drug.name] += purchase









