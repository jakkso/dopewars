"""
Contains city implementations
"""
from dopewars.vendors import *


class City:
    """
    Parent for all cities.
    Holds name
    """

    def __init__(self, name: str) -> None:
        """

        :param name: city name, string
        """
        self.name = name

    def __str__(self):
        return f"{self.__class__.__name__}"


class Miami(City):
    """
    """

    def __init__(self):
        super().__init__("Miami")
