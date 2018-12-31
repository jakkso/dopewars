"""
Contains stores
"""
from typing import List


class Store:
    """
    Buy stuff from stores!
    """

    def __init__(self) -> None:
        self.inventory: List[Weapon] = None

    def __str__(self) -> str:
        return f"{self.__class__.__name__}"


class Walmart(Store):
    def __init__(self):
        super(Walmart, self).__init__()
        self.inventory = [Gun(), Knife()]


class CIA(Store):
    def __init__(self):
        super(CIA, self).__init__()
        self.inventory = [Blackmail()]


class Weapon:
    """
    Weapons protect against loss of money and drugs.
    When they protect the player, they are lost
    """

    def __init__(self, name: str, price: int):
        self.name = name
        self.price = price

    def __str__(self) -> str:
        return f"{self.__class__.__name__}"

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return self.name == other.name
        return False

    def __ne__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return self.name != other.name
        return False

    @staticmethod
    def defeat(opponent: str) -> bool:
        """

        :param opponent:
        :return:
        """
        return False


class Knife(Weapon):
    """
    Prevents thieves from stealing money
    """

    def __init__(self):
        super(Knife, self).__init__("Knife", 20)

    @staticmethod
    def defeat(opponent: str) -> bool:
        """
        :param opponent:
        :return:
        """
        return opponent == "robber"


class Gun(Weapon):
    """
    Prevents Corrupt cops from taking drugs and thieves from taking money
    """

    def __init__(self):
        super(Gun, self).__init__("Glock", 500)

    @staticmethod
    def defeat(opponent: str) -> bool:
        """
        :param opponent:
        :return:
        """
        return opponent == "robber" or opponent == "corrupt cop"


class Blackmail(Weapon):
    """
    Prevents Good Cops from causing the player to instantly lose
    """

    def __init__(self):
        super(Blackmail, self).__init__("Blackmail", 100_000)

    @staticmethod
    def defeat(opponent: str) -> bool:
        return opponent == "good cop"
