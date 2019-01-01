"""
Contains gameplay implementation
"""
import os
from string import ascii_letters as alpha

from dopewars.cities import (
    City,
    Miami,
    NYC,
    Atlanta,
    Seattle,
    Chicago,
    LosAngeles,
    Washington,
)
from dopewars.day import Day
from dopewars.player import Player
from dopewars.scores import Scores
from dopewars.utilities import fmt_money


class Gameplay:
    """
    Instantiates all the other objects required to play the game:
    draws menus; accepts and validates user input; transforms user
    input into data manipulation
    """

    menu_width = 36

    def __init__(self, days: int = 30) -> None:
        self.days = days
        self.player = None
        self.cities: dict[str:City] = None
        self.current_city: City = None
        self.current_day_num: int = None
        self.current_day: Day = None
        self.name: str = None
        self.score = None
        self._score_file = "scores.csv"
        self.start_menu()

    def __str__(self) -> str:
        return f"Gameplay {self.current_day} in {self.current_city}"

    def _generate_cities(self) -> None:
        """
        :return:
        """
        self.cities = {
            "Miami": Miami(),
            "NYC": NYC(),
            "Atlanta": Atlanta(),
            "Chicago": Chicago(),
            "LA": LosAngeles(),
            "Seattle": Seattle(),
            "Washington D.C.": Washington(),
        }
        self.current_city = self.cities["Miami"]

    @staticmethod
    def clear() -> None:
        """
        Clears the screen.
        """
        os.system("cls" if os.name == "nt" else "clear")
        print("\n" * 100)

    @staticmethod
    def logo() -> None:
        """
        Prints this totally awesome ASCII Logo
        """

        print(
            """
    ▓█████▄  ▒█████   ██▓███  ▓█████     █     █░ ▄▄▄       ██▀███    ██████ 
    ▒██▀ ██▌▒██▒  ██▒▓██░  ██▒▓█   ▀    ▓█░ █ ░█░▒████▄    ▓██ ▒ ██▒▒██    ▒ 
    ░██   █▌▒██░  ██▒▓██░ ██▓▒▒███      ▒█░ █ ░█ ▒██  ▀█▄  ▓██ ░▄█ ▒░ ▓██▄   
    ░▓█▄   ▌▒██   ██░▒██▄█▓▒ ▒▒▓█  ▄    ░█░ █ ░█ ░██▄▄▄▄██ ▒██▀▀█▄    ▒   ██▒
    ░▒████▓ ░ ████▓▒░▒██▒ ░  ░░▒████▒   ░░██▒██▓  ▓█   ▓██▒░██▓ ▒██▒▒██████▒▒
     ▒▒▓  ▒ ░ ▒░▒░▒░ ▒▓▒░ ░  ░░░ ▒░ ░   ░ ▓░▒ ▒   ▒▒   ▓▒█░░ ▒▓ ░▒▓░▒ ▒▓▒ ▒ ░
     ░ ▒  ▒   ░ ▒ ▒░ ░▒ ░      ░ ░  ░     ▒ ░ ░    ▒   ▒▒ ░  ░▒ ░ ▒░░ ░▒  ░ ░
     ░ ░  ░ ░ ░ ░ ▒  ░░          ░        ░   ░    ░   ▒     ░░   ░ ░  ░  ░  
       ░        ░ ░              ░  ░       ░          ░  ░   ░           ░  
"""
        )

    def main_menu(self) -> None:
        """
        Draws start menu
        """
        self.clear()
        self.logo()
        print("Remember 10th grade math?  Neither do I, because of this game.\n")
        print("1) New Game")
        print("2) Quit")

    def start_menu(self) -> None:
        """
        Handles user interaction to start game or quit
        """

        def check_alpha(name: str) -> bool:
            """
            Checks that only ascii letters are in name
            :param name:
            :return:
            """
            for char in name:
                if char not in alpha:
                    return False
            return True

        self.main_menu()
        valid_answers = ("1", "2")
        while True:
            answer = input("What would you like to do: ")
            if answer in valid_answers:
                break
        if answer == "1":
            while True:
                ans = input("How many turns: ")
                try:
                    self.days = int(ans)
                    while True:
                        name = input("Name: ")
                        if not check_alpha(name):
                            print("Letters only please")
                            continue
                        else:
                            self.name = name
                            break
                    self.run()
                except ValueError:
                    continue
        elif answer == "2":
            quit(0)

    def play_menu(self) -> None:
        """
        Draws the play menu.  This can be repeatedly called by Gameplay.sell_menu
        and Gameplay.buy_menu in order for the player to go back and forth between
        the menus without ending that turn.
        """
        event = self.current_day.event_text
        if event:
            self.clear()
            input(event)
            self.current_day.event_text = None
        self.clear()
        print("=" * Gameplay.menu_width)
        print(f"Day {self.current_day_num}")
        print(self.current_city.name)
        print(fmt_money(self.player.money))
        print("=" * Gameplay.menu_width)
        self.player.print_inv()
        print("=" * Gameplay.menu_width)
        self.current_day.print_offerings()
        print("=" * Gameplay.menu_width)
        print("1) Buy")
        print("2) Sell")
        if self.current_city.bank:
            valid = "1", "2", "3", "4"
            print("3) Visit Bank")
            print("4) Move")
        elif self.current_city.store:
            valid = "1", "2", "3", "4"
            print(f"3) Visit {self.current_city.store}")
            print("4) Move")
        else:
            valid = "1", "2", "3"
            print("3) Move")
        print("=" * Gameplay.menu_width)
        while True:
            choice = input("What do you want to do: ")
            if choice in valid:
                break
        if choice == "1":
            self.buy_menu()
        elif choice == "2":
            self.sell_menu()
        elif (
            choice == "3" and not self.current_city.bank and not self.current_city.store
        ):
            self.move_menu()
        elif choice == "3" and self.current_city.bank and not self.current_city.store:
            self.bank_menu()
        elif choice == "3" and self.current_city.store and not self.current_city.bank:
            self.store_menu()
        elif choice == "4" and (self.current_city.bank or self.current_city.store):
            self.move_menu()
        else:
            input(f"{choice} {self.current_city.store}")

    def sell_menu(self) -> None:
        """
        Draws sell menu, handles player input
        """
        if not self.player.inv:
            input("You have nothing to sell.")
            return self.play_menu()
        choices = {}
        for index, (key, value) in enumerate(self.player.inv.items()):
            index += 1
            price = self.current_day.get_price(key)
            print(f"{index}) {value.name} | ${price} | {value.quantity}")
            choices[str(index)] = value.name, price
        choices["c"] = "cancel"
        while True:
            choice = input("Sell which (c to cancel): ")
            if choice in choices:
                break
        if choice == "c":
            return self.play_menu()
        name, price = choices[choice]
        while True:
            amount = input("How many (c to cancel): ")
            if amount == "c":
                return self.play_menu()
            try:
                amount = int(amount)
                self.current_day.sell(name, amount)
                break
            except ValueError:
                continue
            except RuntimeError as e:
                print(str(e))
        return self.play_menu()

    def buy_menu(self) -> None:
        """
        Draws buy menu, handles player input
        """
        self.clear()
        print("=" * Gameplay.menu_width)
        self.current_day.print_offerings()
        print("=" * Gameplay.menu_width)
        print(fmt_money(self.player.money))
        drugs = self.current_day.get_drugs()
        choices = {}
        for index, drug in enumerate(drugs):
            choices[str(index + 1)] = drug
        choices["c"] = "cancel"
        while True:
            choice = input("Which do you want to buy (c to cancel): ")
            if choice in choices:
                break
        if choice == "c":
            return self.play_menu()
        while True:
            try:
                amount = input("How many (c to cancel): ")
                if amount == "c":
                    return self.play_menu()
                amount = int(amount)
                self.current_day.buy(choices[choice], amount)
                break
            except ValueError:
                continue
            except RuntimeError as e:
                print(str(e))
        return self.play_menu()

    def bank_menu(self) -> None:
        """
        Draws the bank interaction menu
        """
        self.clear()
        print("=" * Gameplay.menu_width)
        print(f"Welcome to {self.current_city.bank.name}")
        print(f"Cash: {fmt_money(self.player.money)}")
        print(f"Bank balance: {fmt_money(self.current_city.bank.balance)}")
        choices = {"1": "Deposit", "2": "Withdraw", "3": "Go back"}
        for key, value in choices.items():
            print(f"{key}) {value}")
        while True:
            choice = input("What do you want to do: ")
            if choice in choices:
                break
        if choice == "1":
            while True:
                amount = input("Amount to deposit: ")
                try:
                    amount = int(amount)
                    if amount > self.player.money:
                        input("Insufficient Funds")
                        return self.bank_menu()
                    msg = self.current_city.bank.deposit(amount)
                    input(msg)
                    self.player.money -= amount
                    return self.bank_menu()
                except ValueError:
                    continue
        elif choice == "2":
            while True:
                amount = input("How much to withdraw (c to cancel): ")
                if amount == "c":
                    return self.bank_menu()
                try:
                    amount = int(amount)
                    withdraw = self.current_city.bank.withdraw(amount)
                    print(f"Withdrew ${withdraw}")
                    self.player.money += withdraw
                    return self.bank_menu()
                except ValueError:
                    continue
        elif choice == "3":
            return self.play_menu()

    def store_menu(self) -> None:
        """
        Draws the store menu
        :return:
        """
        self.clear()
        print("=" * Gameplay.menu_width)
        print("Here are the offerings")
        choices = {}
        for index, weapon in enumerate(self.current_city.store.inventory):
            index += 1
            choices[str(index)] = weapon
            print(f"{index}) | {weapon.name} | {weapon.price}")
        choices["c"] = None
        while True:
            choice = input("What do you want to buy (c to cancel): ")
            if choice in choices:
                break
        if choice == "c":
            return self.play_menu()
        try:
            weapon = choices[choice]
            self.player.weapon = weapon
        except RuntimeError as e:
            input(e)
        return self.play_menu()

    def move_menu(self) -> None:
        """
        Draws move menu, handles player input.
        This ends this day's turn
        """
        available_cities = [
            city for name, city in self.cities.items() if self.current_city != city
        ]
        self.clear()
        print("=" * Gameplay.menu_width)
        choices = {}
        for index, city in enumerate(available_cities):
            index += 1
            print(f"{index}) {city.name}")
            choices[str(index)] = city
        while True:
            choice = input("Destination: ")
            if choice in choices:
                break
        self.current_city = choices[choice]

    def _final_score(self) -> int:
        """
        Sums up all the money deposited in the various banks
        """
        s = 0
        for _, city in self.cities.items():
            if city.bank:
                s += city.bank.balance
        return s

    def _calc_interest(self) -> None:
        """
        Called on each iteration of the turn
        :return:
        """
        for _, city in self.cities.items():
            if city.bank:
                city.bank.calc_interest()

    def _print_scores(self) -> None:
        """
        Prints score from current game, as well as high scores
        """
        self.clear()
        score = self._final_score()
        score_text = f"Final score: {fmt_money(score)}"
        print(score_text)
        s = Scores()
        s.add((score, self.player.name))
        s.save()
        s.print()
        input()

    def run(self) -> None:
        """
        Starts and runs the game.
        """
        self.clear()
        self.player = Player(self.name, 500)
        self._generate_cities()
        for n in range(1, self.days + 1):
            self._calc_interest()
            self.current_day_num = n
            day = Day(self.current_city, self.player)
            self.current_day = day
            if day.end_game:
                input(day.event_text)
                break
            self.play_menu()
        self._print_scores()
        return self.start_menu()
