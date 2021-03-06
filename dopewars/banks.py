"""Contain bank implementation."""

from dopewars.utilities import fmt_money


class Bank:
    """Hold player's money, calculate interest on deposits.

    Banks can have minimum deposits, with which come higher interest rates.
    """

    def __init__(
        self, name: str, interest_rate: float, min_deposit: int = None
    ) -> None:
        self.name = name
        self._interest_rate: float = interest_rate
        self._balance: int = 0
        self._min_deposit = min_deposit
        self._initial_deposit = True

    def __str__(self):
        return f"{self.__class__.__name__}"

    def deposit(self, amount: int) -> str:
        """Increment Bank.balance by `amount`.

        :param amount: int
        """
        if self._initial_deposit:
            if self._min_deposit:
                if amount < self._min_deposit:
                    return f"Amount must be greater than {fmt_money(self._min_deposit)}"
                else:
                    self._initial_deposit = False
        self._balance += amount
        return f"Balance: {fmt_money(self.balance)}"

    def withdraw(self, amount: int) -> int:
        """Decrement Bank.balance by `amount`.

        :param amount: int
        :return: int returns amount withdrawn
        """
        if amount > self._balance:
            return 0
        self._balance -= amount
        return amount

    @property
    def balance(self) -> int:
        """Return balance."""
        return self._balance

    def calc_interest(self) -> None:
        """Calculate compounded interest."""
        self._balance += int(self._balance * self._interest_rate)


class TexasMidland(Bank):
    """
    No min deposit
    1% interest
    """

    def __init__(self):
        super().__init__(name="Texas Midland Bank", interest_rate=0.01)


class BoAConstrictor(Bank):
    """
    50,000 min deposit
    4% Interest
    """

    def __init__(self):
        super().__init__(name="BoA Constrictor", interest_rate=0.04, min_deposit=50000)


class LehmanSis(Bank):
    """
    250,000 min deposit
    6% Interest
    """

    def __init__(self):
        super().__init__(name="Lehman Sisters", interest_rate=0.06, min_deposit=250_000)


class GoldmanSacks(Bank):
    """
    Hehe Sacks
    1,000,000 min deposit
    10% Interest
    """

    def __init__(self):
        super().__init__(
            name="Goldman Sacks", interest_rate=0.08, min_deposit=1_000_000
        )
