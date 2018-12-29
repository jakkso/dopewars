"""
Contains Drug
"""
from random import randint


class InventoryDrug:
    """
    This class defines how a drug held in a player's inventory behaves.
    Holds quantity, contains method to manage selling it
    """

    def __init__(self, name: str, quantity: int) -> None:
        """
        :param name: Drug's name
        :param quantity: amount of drug
        """
        self.name = name
        self.quantity = quantity

    def __str__(self):
        return f"{self.name}: {self.quantity}"

    def sell(self, sale_quant, sale_price: int) -> int:
        """
        Reduces InventoryDrug._quantity by sale_quant, if it is larger than
        sale_quant, returns the amount made by the sale, returns value of sale
        :param sale_price: int > 0
        :param sale_quant: amount to attempt to sell
        :return value of sale
        """
        if sale_quant <= 0 or sale_price < 0:
            raise RuntimeError("Sale price and quantities must be greater than zero")
        if self.quantity < sale_quant:
            raise RuntimeError("Insufficient quantity")
        self.quantity -= sale_quant
        return sale_quant * sale_price

    def __add__(self, other):
        """
        Defines how to add two InventoryDrug classes together
        :param other:
        :return:
        """
        if other.__class__.__name__ != "InventoryDrug":
            raise RuntimeError(
                f"Invalid target for addition: {other.__class__.__name__}"
            )
        if self.name != other.name:
            return self
        self.quantity += other.quantity
        other.quantity = 0
        return self


class Drug:
    """
    Defines how drug's price and quantities are generated.
    This class is used for buying only.
    """

    def __init__(self, name: str, base_price: int, jitter: int) -> None:
        """
        :param name: Drug's name
        :param base_price: base price of drug
        :param jitter: amount of units around base_price to jitter, defines
            volatility
        surge: set when instantiated, can be `hi`, `lo` or None.
            If set to hi, the base price is modified to be 1.5-3x as much
            If set to lo, the base price is modified to be 1/3 - 2/3 as much
        """
        if base_price <= 0 or jitter <= 0:
            raise RuntimeError("Price and jitter must be larger than 0")
        self._base_price = base_price
        self.name = name
        self._jitter = jitter
        self._surge = None
        self.price = None
        self.quantity = None
        self._calc_surge()
        self._calc_price()
        self._calc_quantity()

    def __str__(self):
        return f"{self.name} price: {self.price}"

    def _calc_price(self) -> None:
        """
        Calculates price for a particular instantiation
        """
        if self._surge == "hi":
            # 1.5-3x as much
            base = self._base_price * randint(15, 30) / 10
        elif self._surge == "lo":
            # 0.33-0.67x as much
            base = self._base_price * randint(33, 67) / 100
        else:
            base = self._base_price

        price = int(base) + randint(-self._jitter, self._jitter)
        self.price = max(
            price, int(0.15 * self._base_price)
        )  # Set a price floor as 15% of base

    def _calc_quantity(self) -> None:
        """
        Calculates amount of drug available for purchase.
        If there is a hi surge, less is available, vice versa for a lo surge
        """
        base_quant = randint(5, 100)
        if self._surge == "hi":
            rv = max(int(base_quant / 3), 8)
        elif self._surge == "lo":
            rv = base_quant * 3
        else:
            rv = base_quant
        self.quantity = rv

    def _calc_surge(self) -> None:
        """
        Calculates whether or not there will be a price surge,
        set's Drug._surge equal to either `lo` or `hi` if there will be
        """
        chance = randint(1, 100)
        if 80 < chance <= 100:
            self._surge = "hi"
        elif 60 < chance <= 80:
            self._surge = "lo"


class Weed(Drug):
    def __init__(self):
        super().__init__(name="Weed", base_price=100, jitter=15)


class Luuds(Drug):
    def __init__(self):
        super().__init__(name="Luuds", base_price=10, jitter=3)


class Coke(Drug):
    def __init__(self):
        super().__init__(name="Coke", base_price=300, jitter=50)


class Molly(Drug):
    def __init__(self):
        super().__init__(name="Molly", base_price=50, jitter=8)


class Shrooms(Drug):
    def __init__(self):
        super().__init__(name="Shrooms", base_price=25, jitter=5)


class Acid(Drug):
    def __init__(self):
        super().__init__(name="Acid", base_price=500, jitter=100)


class Meth(Drug):
    def __init__(self):
        super().__init__(name="Meth", base_price=800, jitter=90)


class Heroin(Drug):
    def __init__(self):
        super().__init__(name="Heroin", base_price=1000, jitter=500)
