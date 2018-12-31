"""
Contains implementation of a Day
"""
from random import choice, randint

from dopewars.cities import City
from dopewars.drugs import Weed, Luuds, Coke, Molly, Shrooms, Acid, Meth, Heroin, Drug
from dopewars.player import Player


class Day:
    """
    Day represents a single turn of the game.  Player can make trades and
    will encounter random events
    """

    def __init__(self, city: City, player: Player) -> None:
        self.city = city
        self.player = player
        self.end_game = False
        self._drugs: dict[str:Drug] = {}
        self.event = None
        self._generate_drugs()
        self._generate_event()

    def __str__(self):
        return f"City {self.city.name}"

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

        def spacer(str_len: int, amount: int) -> str:
            """
            Pads string length with spaces to create a uniformly spaced grid
            :param str_len: int length of string
            :param amount: int length up to which to pad
            :return: spaces and a `|` at the end of the spacer
            """
            return ((amount - str_len) * " ") + "|"

        title_bar = "#) | Drug    | Price | Avail | Max |"
        print(title_bar)
        print(len(title_bar) * "+")
        for index, (_, drug) in enumerate(self._drugs.items()):
            max_amount = min((self.player.money // drug.price), drug.quantity)
            name = f"{index + 1}) | {drug.name}"
            name = "".join([name, spacer(len(name), 13)])
            price = f"${drug.price}{spacer(len(str(drug.price)), 5)}"
            avail = f"{drug.quantity}{spacer(len(str(drug.quantity)), 6)}"
            max_amt = f"{max_amount} {spacer(len(str(max_amount)), 3)}"
            print(f"{name} {price} {avail} {max_amt}")

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
            Corrupt Cop
             * TODO Takes all product if player doesn't bribe them for max(500, 10% of money)
            Untouchable Cop
             * Takes all product, end game
             * If you have no product, you're free to go
        Can only have one type of event happen per turn, one is randomly chosen
        """

        def get_chance(number: int) -> bool:
            """
            Gets random number from 1-number, returns if the number chosen is 1
            :param number:
            """
            return randint(1, number) == 1

        event, value = choice(list({"robber": 3, "bod_cop": 5, "good_cop": 50}.items()))
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
