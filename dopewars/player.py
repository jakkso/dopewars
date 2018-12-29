"""
Contains Player definition
"""
from random import choice, randint

from dopewars.drugs import Drug, InventoryDrug


class Player:
    """
    Defines how the player works, contains money and inventory
    """

    def __init__(self, name: str, money: int) -> None:
        self.name = name
        self._money = money
        self.inv: dict[str:InventoryDrug] = {}

    def __str__(self):
        return f"{self.name}: {self.money}"

    @property
    def money(self):
        return self._money

    def buy(self, drug: Drug, quantity: int) -> None:
        """
        :param quantity:
        :param drug:
        :return:
        """
        if quantity > drug.quantity or quantity <= 0:
            raise RuntimeError("Insufficient quantity")
        price = quantity * drug.price
        if self._money < price:
            raise RuntimeError("Insufficient funds")
        purchase = InventoryDrug(drug.name, quantity)
        drug.quantity -= quantity
        if self.inv.get(drug.name) is None:
            self.inv[drug.name] = purchase
        else:
            self.inv[drug.name] += purchase
        self._money -= price

    def sell(self, drug_name: str, quantity: int, price: int) -> None:
        """
        Implements sale logic
        :param drug_name:
        :param quantity:
        :param price:
        :return:
        """
        if self.inv.get(drug_name) is None:
            raise RuntimeError("Drug not found")  # Shouldn't be needed?
        self._money += self.inv[drug_name].sell(quantity, price)
        if self.inv[drug_name].quantity == 0:
            del self.inv[drug_name]

    def print_inv(self) -> None:
        """
        Prints styled contents of inventory
        """
        if len(self.inv) == 0:
            print("You have nothing.")
        else:
            for key, value in self.inv.items():
                print(f"{key}: {value.quantity}")

    def steal_money(self) -> str:
        """
        When called, randomly removes 5-15% of money and decrements it from self._money
        :return string describing what was removed
        """
        stolen = int(randint(5, 15) / 100 * self._money)
        self._money -= stolen
        return f'A thief stole {stolen} from you!'

    def steal_drugs(self) -> str:
        """
        When called, randomly deletes some drugs from player's inventory
        Randomly select a drug from inv, remove 25% of that drug
        :return string describing what was removed
        """
        if not self.inv:
            return 'Nothing to take!'
        name, drug = choice(list(self.inv.items()))
        quantity = int(drug.quantity / 4)
        self.sell(name, quantity, price=0)
        return f'{quantity} of {name} were confiscated!'


