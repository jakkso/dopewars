"""
Contains Drug
"""
from random import randint


class Drug:
    """
    Defines how drug's price and quantities are generated.
    This class is used for buying only.
    """
    def __init__(self,
                 name: str,
                 base_price: int,
                 jitter: int,
                 surge: str=None) -> None:
        """
        :param name: Drug's name
        :param base_price: base price of drug
        :param jitter: amount of units around base_price to jitter, defines
            volatility
        :param surge: set when instantiated, can be `hi`, `lo` or None.
            If set to hi, the base price is modified to be 1.5-3x as much
            If set to lo, the base price is modified to be 1/3 - 2/3 as much
        """
        self._base_price = base_price
        self.name = name
        self._jitter = jitter
        self._surge = surge
        self.price = None
        self.quantity = None
        self._calc_price()
        self._calc_quantity()

    def __str__(self):
        return f'{self.name} price: {self.price}'

    def _calc_price(self) -> None:
        """
        Calculates price for a particular instantiation
        """
        if self._surge == 'hi':
            # 1.5-3x as much
            base = self._base_price * randint(15, 30) / 10
        elif self._surge == 'lo':
            # 0.33-0.67x as much
            base = self._base_price * randint(33, 67) / 100
        else:
            base = self._base_price

        price = int(base) + randint(-self._jitter, self._jitter)
        self.price = max(price, int(0.15 * self._base_price))  # Set a price floor as 15% of base

    def _calc_quantity(self) -> None:
        """
        Calculates amount of drug available for purchase.
        If there is a hi surge, less is available, vice versa for a lo surge
        """
        base_quant = randint(5, 50)
        if self._surge == 'hi':
            rv = max(int(base_quant / 3), 8)
        elif self._surge == 'lo':
            rv = base_quant * 3
        else:
            rv = base_quant
        self.quantity = rv


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
        self._name = name
        self._quantity = quantity

    def __str__(self):
        return f'{self._name}: {self._quantity}'

    def sell(self, sale_quant, sale_price: int) -> int:
        """
        Reduces InventoryDrug._quantity by sale_quant, if it is larger than
        sale_quant, returns the amount made by the sale, returns value of sale
        :param sale_price: int > 0
        :param sale_quant: amount to attempt to sell
        :return value of sale
        """
        if self._quantity < sale_quant:
            return 0
        self._quantity -= sale_quant
        return sale_quant * sale_price



