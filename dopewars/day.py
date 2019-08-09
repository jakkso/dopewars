"""
Contains implementation of a Day
"""
from random import choice, randint

from dopewars.cities import City
from dopewars.drugs import Drug, DRUGS
from dopewars.player import Player


class Day:
    """Represent a single turn of the game.

    Player can make trades and will encounter random events.
    """

    def __init__(self, city: City, player: Player) -> None:
        self.city = city
        self.player: Player = player
        self.end_game: bool = False
        self._drugs: dict[str:Drug] = {}
        self.event_text: str = None
        self.event_name: str = None
        self._generate_drugs()
        self._generate_event()

    def __str__(self):
        return f"City {self.city.name}"

    def _generate_drugs(self) -> None:
        """Generate list of drugs available for purchase for this particular day."""
        for drug in DRUGS:
            d = drug()
            self._drugs[d.name] = d

    def buy(self, drug: str, quantity: int) -> None:
        """Create interface for player to buy a drug.

        Decrements the amount available upon purchase.
        :param drug: str
        :param quantity: int
        """
        if self._drugs.get(drug) is None:
            return
        self.player.buy_drugs(self._drugs[drug], quantity)

    def sell(self, drug: str, quantity: int) -> None:
        """Create interface for player to sell a drug.

        :param drug: drug name
        :param quantity: quantity to sell
        """
        price = self._drugs[drug].price
        self.player.sell(drug, quantity, price)

    def get_drugs(self):
        """Return available drugs.

        Day._drugs has a signature of dict[str: Drug]
        """
        return self._drugs

    def print_offerings(self) -> None:
        """Print current offerings amounts and prices."""

        def spacer(str_len: int, amount: int) -> str:
            """Pad string length with spaces to create a uniformly spaced grid.

            :param str_len: int length of string
            :param amount: int length up to which to pad
            :return: spaces and a `|` at the end of the spacer
            """
            return ((amount - str_len) * " ") + "|"

        title_bar = "#)  | Item     | Price   | Avail | Max |"
        print(title_bar)
        print(len(title_bar) * "+")
        for index, (_, drug) in enumerate(self._drugs.items()):
            spaces = "  " if index + 1 <= 9 else " "
            max_amount = min((self.player.money // drug.price), drug.quantity)
            name = f"{index + 1}){spaces}| {drug.name}"
            name = "".join([name, spacer(len(name), 15)])
            price = f"{drug.formatted_price}{spacer(len(str(drug.formatted_price)), 8)}"
            avail = f"{drug.quantity}{spacer(len(str(drug.quantity)), 6)}"
            max_amt = f"{max_amount} {spacer(len(str(max_amount)), 3)}"
            print(f"{name} {price} {avail} {max_amt}")

    def get_price(self, drug: str) -> int:
        """Return price of a specific drug.

        :param drug: name of drug, str
        :return price of drug, int
        """
        return self._drugs[drug].price

    def _generate_event(self) -> None:
        """Randomly generates events.

        There are three types of events:
            Robber
             * Takes a little money / product from player
            Corrupt Cop
             * Takes percentage of product if player doesn't have a Gun
            Untouchable Cop
             * Takes all product, end game
             * If you have no product, you're free to go
        Can only have one type of event happen per turn, one is randomly chosen
        """

        def get_chance(number: int) -> bool:
            """ Return if a randomly chosen number is 1

            :param number:
            """
            return randint(1, number) == 1

        event, value = choice(
            list({"robber": 3, "corrupt cop": 5, "good cop": 50}.items())
        )
        chance = get_chance(value)
        if not chance:
            return
        self.event = event
        if self.player.weapon:
            if self.player.weapon.defeat(event):
                self.event_text = (
                    f"You were accosted by a {event}, but managed"
                    f" to defend yourself using your {self.player.weapon}"
                )
                self.player.weapon = None
                return
        if event == "robber":
            self.event_text = self.player.steal_money()
        elif event == "corrupt cop":
            self.event_text = f"A corrupt cop stopped you!\n{self.player.steal_drugs()}"
        else:
            if self.player.inv:
                self.end_game = True
                self.event_text = "The ultimate boy scout cop got you, game over!"
