"""
Contains gameplay implementation
"""

import os

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
from dopewars.utilities import fmt_money


class Gameplay:
    """
    Instantiates all the other objects required to play the game:
    draws menus; accepts and validates user input; transforms user
    input into data manipulation
    """

    def __init__(self, days: int = 30) -> None:
        self.days = days
        self.player = None
        self.cities = {
            "Miami": Miami(),
            "NYC": NYC(),
            "Atlanta": Atlanta(),
            "Chicago": Chicago(),
            "LA": LosAngeles(),
            "Seattle": Seattle(),
            "Washington D.C.": Washington(),
        }
        self.current_city: City = self.cities["Miami"]  # You start in Miami
        self.current_day_num: int = None
        self.current_day: Day = None
        self.score = None
        self.start_menu()

    def __str__(self) -> str:
        return f"Gameplay {self.current_day} in {self.current_city}"

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

    def draw_start_menu(self) -> None:
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
        self.draw_start_menu()
        valid_answers = ("1", "2")
        while True:
            answer = input("What would you like to do: ")
            if answer in valid_answers:
                break
        if answer == "1":
            self.run()
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
        print("=" * 36)
        print(f"Day {self.current_day_num}")
        print(self.current_city.name)
        print(fmt_money(self.player.money))
        print("=" * 36)
        print("Inventory")
        self.player.print_inv()
        print("=" * 36)
        self.current_day.print_offerings()
        print("=" * 36)
        print("1) Buy")
        print("2) Sell")
        if self.current_city.bank:
            valid = "1", "2", "3", "4"
            print("3) Visit Bank")
            print("4) Move")
        elif self.current_city.store:
            valid = "1", "2", "3", "4"
            print(f'3) Visit {self.current_city.store}')
            print("4) Move")
        else:
            valid = "1", "2", "3"
            print("3) Move")
        print("=" * 36)
        while True:
            choice = input("What do you want to do: ")
            if choice in valid:
                break
        if choice == "1":
            self.buy_menu()
        elif choice == "2":
            self.sell_menu()
        elif choice == "3" and not self.current_city.bank and not self.current_city.store:
            self.move_menu()
        elif choice == "3" and self.current_city.bank and not self.current_city.store:
            self.bank_menu()
        elif choice == '3' and self.current_city.store and not self.current_city.bank:
            self.store_menu()
        elif choice == '4' and (self.current_city.bank or self.current_city.store):
            self.move_menu()
        else:
            input(f'{choice} {self.current_city.store}')

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
        print("=" * 36)
        self.current_day.print_offerings()
        print("=" * 36)
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
        print('=' * 36)
        print(f'Welcome to {self.current_city.bank.name}')
        print(f"Current balance: {fmt_money(self.current_city.bank.balance)}")
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
        print('=' * 36)
        print('Here are the offerings')
        choices = {}
        for index, weapon in enumerate(self.current_city.store.inventory):
            index += 1
            choices[str(index)] = weapon
            print(f'{index}) | {weapon.name} | {weapon.price}')
        choices['c'] = None
        while True:
            choice = input('What do you want to buy (c to cancel): ')
            if choice in choices:
                break
        if choice == 'c':
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
        print("=" * 36)
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

    def _final_score(self) -> str:
        """
        Sums up all the money deposited in the various banks
        """
        s = 0
        for _, city in self.cities.items():
            if city.bank:
                s += city.bank.balance
        return f'Final score: {fmt_money(s)} '

    def run(self) -> None:
        """
        Starts and runs the game.
        """
        self.clear()
        self.player = Player("", 500)
        for n in range(1, self.days + 1):
            self.current_day_num = n
            day = Day(self.current_city, self.player)
            self.current_day = day
            if day.end_game:
                input(day.event_text)
                break
            self.play_menu()
        print(self._final_score())
        input()
        return self.start_menu()
