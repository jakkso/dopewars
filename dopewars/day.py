"""
Contains implementation of a Day
"""
from dopewars.drugs import Weed, Luuds, Coke, Molly, Shrooms, Acid, Meth, Heroin, Drug
from dopewars.player import Player


class Day:
    """
    Day represents a single turn of the game.  Player can make trades and (eventually)
    will encounter random events
    """

    def __init__(self, city: str, player: Player) -> None:
        self.city = city
        self.player = player
        self._drugs: dict[str:Drug] = {}
        self._generate_drugs()

    def __str__(self):
        return f"City {self.city}"

    def _generate_drugs(self) -> None:
        """
        Generates random list of drugs available for purchase for this particular day
        """
        for drug in [Weed, Luuds, Coke, Molly, Shrooms, Acid, Meth, Heroin]:
            d = drug()
            self._drugs[d.name] = d

    def buy(self, drug: str, quantity: int) -> None:
        """
        Interface for player to buy a drug.
        Decrements the amount available upon purchase.
        :param drug: str
        :param quantity: int
        """
        if self._drugs.get(drug) is None:
            return
        self.player.buy(self._drugs[drug], quantity)

    def sell(self, drug: str, quantity: int) -> None:
        """
        Interface for player to sell a drug
        :param drug:
        :param quantity:
        """
        price = self._drugs[drug].price
        self.player.sell(drug, quantity, price)

    def get_drugs(self):
        """
        Day._drugs has a signature of dict[str: Drug]
        """
        return self._drugs

    def print_offerings(self) -> None:
        """
        Prints current offerings amounts and price
        """
        print("Drug | Price | Quantity")
        print("-" * 20)
        for index, (_, drug) in enumerate(self._drugs.items()):
            print(f"{index + 1}) {drug.name} | ${drug.price} | {drug.quantity}")

    def get_price(self, drug: str) -> int:
        """
        :param drug: name of drug, str
        :return price of drug, int
        """
        return self._drugs[drug].price
