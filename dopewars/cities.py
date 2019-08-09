"""
Contains city implementations
"""
from dopewars.banks import Bank, BoAConstrictor, GoldmanSacks, LehmanSis, TexasMidland
from dopewars.weapons import CIA, Store, Walmart


class City:
    """Parent for all cities.

    Holds name, as well as vendors.
    """

    def __init__(self, name: str, **kwargs) -> None:
        """

        :param name: city name, string
        """
        self.name = name
        self.bank: Bank = kwargs.get("bank", None)
        self.store: Store = kwargs.get("store", None)

    def __str__(self):
        return f"{self.__class__.__name__} {self.name}"

    @classmethod
    def miami(cls):
        return cls("Miami", bank=BoAConstrictor())

    @classmethod
    def nyc(cls):
        return cls("NYC", bank=GoldmanSacks())

    @classmethod
    def atlanta(cls):
        return cls("Atlanta", bank=TexasMidland())

    @classmethod
    def chicago(cls):
        return cls("Chicago", bank=LehmanSis())

    @classmethod
    def los_angeles(cls):
        return cls("LA", store=Walmart())

    @classmethod
    def seattle(cls):
        return cls("Seattle", store=Walmart())

    @classmethod
    def washington(cls):
        return cls("Washington, D.C.", store=CIA())
