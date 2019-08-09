"""
Contains Player definition
"""
from random import choice, randint

from dopewars.drugs import Drug, InventoryDrug
from dopewars.weapons import Weapon


class Player:
    """
    Defines how the player works, contains money and inventory
    """

    def __init__(self, name: str, money: int) -> None:
        self.name = name
        self._money = money
        self.inv: dict[str:InventoryDrug] = {}
        self._weapon: Weapon = None

    def __str__(self):
        return f"{self.name}: {self.money}"

    @property
    def money(self) -> int:
        return self._money

    @money.setter
    def money(self, value: int) -> None:
        """
        Setter for Player._money
        :param value:
        :return:
        """
        if value < 0:
            return
        self._money = value

    @property
    def weapon(self) -> Weapon:
        """Getter for Player._weapon."""
        return self._weapon

    @weapon.setter
    def weapon(self, weapon: Weapon) -> None:
        """Setter for Player._weapon.

        :param weapon:
        """
        if weapon is None:
            self._weapon = None
            return
        elif not isinstance(weapon, Weapon):
            return
        elif self._money < weapon.price:
            raise RuntimeError("Insufficient funds")
        self.money -= weapon.price
        self._weapon = weapon

    def buy_drugs(self, drug: Drug, quantity: int) -> None:
        """Implement drug buying interface.

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
        """Implement drug sale interface.

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
        """Print styled contents of inventory."""
        if self.weapon:
            print(f"Weapon: {self.weapon}")
            print("-" * 36)
        print("Inventory")
        if not self.inv:
            print("You have no product.")
        else:
            for key, value in self.inv.items():
                print(f"{key}: {value.quantity}")

    def steal_money(self) -> str:
        """Steal money from player.

        When called, randomly removes 5-15% of money
        :return string describing what was removed.
        """
        amount = int(randint(5, 15) / 100 * self._money)
        if amount == 0:
            return "A thief tried to steal from you, but you are flat broke!"
        self._money -= amount
        return f"A thief stole {amount} from you!"

    def steal_drugs(self) -> str:
        """Steal drugs from player.

        When called, randomly deletes some drugs from player's inventory
        Randomly select a drug from inv, remove 25% of that drug
        :return string describing what was removed
        """
        if not self.inv:
            return "Nothing to take!"
        name, drug = choice(list(self.inv.items()))
        quantity = max(1, int(drug.quantity / 4))
        self.sell(name, quantity, price=0)
        return f"{quantity} of {name} were confiscated!"
