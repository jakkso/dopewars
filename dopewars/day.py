"""
Contains implementation of a Day
"""
from dopewars.drugs import Weed, Luuds, Coke, Molly, Shrooms, Acid, Meth, Heroin, Drug
from dopewars.player import Player

from random import choice, randint


class Day:
    """
    Day represents a single turn of the game.  Player can make trades and
    will encounter random events
    """

    def __init__(self, city: str, player: Player) -> None:
        self.city = city
        self.player = player
        self.end_game = False
        self._drugs: dict[str:Drug] = {}
        self.event = None
        self._generate_drugs()
        self._generate_event()

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

    def _generate_event(self) -> None:
        """
        Randomly generates events
        There are three types of events:
            Robber
             * Takes a little money / product from player
             * 1/50 chance
            Corrupt Cop
             * Takes all product if player doesn't bribe them for max(500, 10% of money)
             * 1/100 chance
            Untouchable Cop
             * Takes all product, end game
             * If you have no product, you're free to go
             * 1/500 chance
        Can only have one type of event happen per turn, one is randomly chosen
        """

        def get_chance(number: int) -> bool:
            """
            Gets random number from 1-number, returns if the number chosen is 1
            :param number:
            """
            return randint(1, number) == 1

        event, value = choice(
            list({"robber": 5, "bod_cop": 10, "good_cop": 100}.items())
        )
        chance = get_chance(value)
        if not chance:
            return
        if event == "robber":
            self.event = self.player.steal_money()
        elif event == "bad_cop":
            self.event = "A corrupt cop stopped you!\n{self.player.steal_drugs()}"
        else:
            if self.player.inv:
                self.end_game = True
                self.event = "The ultimate boy scout cop got you, game over!"
