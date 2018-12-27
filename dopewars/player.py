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

    def sell(self, drug_name: str, quantity: int, price: int) -> None:
        """
        Implements sale logic
        :param drug_name:
        :param quantity:
        :param price:
        :return:
        """
        if self.inv.get(drug_name) is None:
            raise RuntimeError('Drug not found')
        self._money += self.inv[drug_name].sell(quantity, price)
        if self.inv[drug_name].quantity == 0:
            del self.inv[drug_name]











