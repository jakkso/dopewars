"""
Contains city implementations
"""
from dopewars.vendors import Bank, BoA, GoldmanSacks, LehmanSis, TexasMidland


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
        self.bank: Bank = None

    def __str__(self):
        return f"{self.__class__.__name__}"


class Miami(City):
    """
    Holds BoA Constrictor bank
    """

    def __init__(self):
        super().__init__("Miami")
        self.bank = BoA()


class NYC(City):
    """
    Holds Goldman Sacks
    """

    def __init__(self):
        super().__init__("NYC")
        self.bank = GoldmanSacks()


class Atlanta(City):
    """
    Holds Texas Midlands Bank
    """

    def __init__(self):
        super().__init__("Atlanta")
        self.bank = TexasMidland()


class Chicago(City):
    """
    Holds Lehman's Sis
    """

    def __init__(self):
        super().__init__("Chicago")
        self.bank = LehmanSis()


class LosAngeles(City):
    """
    No vendors as of yet
    """

    def __init__(self):
        super().__init__("LA")


class Seattle(City):
    """
    No vendors as of yet
    """

    def __init__(self):
        super().__init__("Seattle")


class Washington(City):
    """
    No vendors as of yet
    """

    def __init__(self):
        super().__init__("Washington D.C.")
