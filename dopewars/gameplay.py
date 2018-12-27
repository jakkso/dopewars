"""
Contains gameplay implementation
"""

import os

from dopewars.day import Day
from dopewars.player import Player


class Gameplay:
    """
    Instantiates all the other objects required to play the game:
    draws menus; accepts and validates user input; transforms user
    input into data manipulation
    """
    def __init__(self, days: int=30) -> None:
        self.days = days
        self.player = None
        self.cities = ['Miami', 'NYC', 'Chicago', 'LA', 'Seattle', 'Washington D.C.', 'Atlanta']
        self.current_city = 'Miami'  # You start in Miami
        self.current_day_num: int = None
        self.current_day: Day = None
        self.score = None
        self.start_menu()

    def __str__(self) -> str:
        return f'Gameplay {self.current_day} in {self.current_city}'

    @staticmethod
    def clear() -> None:
        """
        Clears the screen.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        print('\n' * 100)

    def draw_start_menu(self) -> None:
        """
        Draws start menu
        """
        self.clear()
        print('Welcome to DopeWars, the subversive game you remember from your TI-83+\n')
        print('1) New Game')
        print('2) Quit')

    def start_menu(self) -> None:
        """
        Handles user interaction to start game or quit
        """
        self.draw_start_menu()
        valid_answers = ('1', '2')
        while True:
            answer = input('What would you like to do: ')
            if answer in valid_answers:
                break
        if answer == '1':
            self.run()
        elif answer == '2':
            quit(0)

    def play_menu(self) -> None:
        """
        Draws the play menu.  This can be repeatedly called by Gameplay.sell_menu
        and Gameplay.buy_menu in order for the player to go back and forth between
        the menus without ending that turn.
        """
        self.clear()
        print('=' * 20)
        print(f'Day {self.current_day_num}')
        print(self.current_city)
        print(f'${self.player.money}')
        print('=' * 20)
        print('Inventory')
        self.player.print_inv()
        print('=' * 20)
        self.current_day.print_offerings()
        print('=' * 20)
        print('1) Buy')
        print('2) Sell')
        print('3) Move')
        print('=' * 20)
        valid = '1', '2', '3'
        while True:
            choice = input('What do you want to do: ')
            if choice in valid:
                break
        if choice == '1':
            self.buy_menu()
        elif choice == '2':
            self.sell_menu()
        elif choice == '3':
            self.move_menu()

    def sell_menu(self) -> None:
        """
        Draws sell menu, handles player input
        """
        if len(self.player.inv) == 0:
            input('You have nothing to sell.')
            return self.play_menu()
        choices = {}
        for index, (key, value) in enumerate(self.player.inv.items()):
            price = self.current_day.get_price(key)
            print(f'{index +1}) {value.name} | ${price} | {value.quantity}')
            choices[str(index + 1)] = value.name, price
        choices['c'] = 'cancel'
        while True:
            choice = input('Sell which (c to cancel): ')
            if choice in choices:
                break
        if choice == 'c':
            return self.play_menu()
        name, price = choices[choice]
        while True:
            amount = input('How many (c to cancel): ')
            if amount == 'c':
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
        print('=' * 20)
        self.current_day.print_offerings()
        drugs = self.current_day.get_drugs()
        choices = {}
        for index, drug in enumerate(drugs):
            choices[str(index + 1)] = drug
        choices['c'] = 'cancel'
        while True:
            choice = input('Which do you want to buy (c to cancel): ')
            if choice in choices:
                break
        if choice == 'c':
            return self.play_menu()
        while True:
            try:
                amount = input('How many (c to cancel): ')
                if amount == 'c':
                    return self.play_menu()
                amount = int(amount)
                self.current_day.buy(choices[choice], amount)
                break
            except ValueError:
                continue
            except RuntimeError as e:
                print(str(e))
        return self.play_menu()

    def move_menu(self) -> None:
        """
        Draws move menu, handles player input.
        This ends this day's turn
        """
        available_cities = filter(lambda item: item != self.current_city, self.cities)
        self.clear()
        print('=' * 20)
        choices = {}
        for index, city in enumerate(available_cities):
            print(f'{index + 1}) {city}')
            choices[str(index + 1)] = city
        while True:
            choice = input('Destination: ')
            if choice in choices:
                break
        self.current_city = choices[choice]

    def run(self) -> None:
        """
        Starts and runs the game.
        """
        self.clear()
        while True:
            name = input('What is your name: ')
            if name.strip():
                break
        self.player = Player(name, 500)
        for n in range(1, self.days):
            self.current_day_num = n
            day = Day(self.current_city, self.player)
            self.current_day = day
            self.play_menu()
        final_score = self.current_day.player.money
        print(f'Final score: {final_score}')
        input()
        return self.start_menu()
