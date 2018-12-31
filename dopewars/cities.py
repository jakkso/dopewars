"""
Contains city implementations
"""
from dopewars.banks import Bank, BoA, GoldmanSacks, LehmanSis, TexasMidland
from dopewars.weapons import CIA, Store, Walmart


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
        self.store: Store = None

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
    Buy a knife or a gun in L.A.!
    """

    def __init__(self):
        super().__init__("LA")
        self.store = Walmart()


class Seattle(City):
    """
    Hey seattle hipsters, buy a glock at walmart!
    """

    def __init__(self):
        super().__init__("Seattle")
        self.store = Walmart()


class Washington(City):
    """
    Visit the CIA!  Blackmail anyone!
    """

    def __init__(self):
        super().__init__("Washington D.C.")
        self.store = CIA()
