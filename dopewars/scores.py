"""
Holds Scores class
"""
import csv
from typing import List, Tuple

from dopewars.utilities import fmt_money


class Scores:
    """Manage storage and retrieval of scores.

    Given that this is run as a docker container, relies
    on a volume being supplied to the `docker run` command
    """

    def __init__(self, file: str = "/app/scores.csv") -> None:
        self._file = file
        self.list: List[Tuple[int, str, int]] = None
        self._read()

    def __str__(self) -> str:
        return f"{self.__class__.__name__}"

    def save(self) -> None:
        """Sort list, write top five scores to disk."""
        self._sort()
        with open(self._file, "w", newline="") as file:
            writer = csv.writer(file, delimiter=" ", quotechar="|")
            for score in self.list:
                writer.writerow(score)

    def _read(self) -> None:
        """Read and convert file to machine-usable data."""
        try:
            with open(self._file, "r", newline="") as file:
                reader = csv.reader(file, delimiter=" ", quotechar="|")
                self.list = [tuple((int(row[0]), row[1], row[2])) for row in reader]
        except FileNotFoundError:
            self.list = []

    def _sort(self) -> None:
        """Sort and trim list."""
        self.list.sort(key=lambda item: item[0], reverse=True)
        if len(self.list) > 5:
            self.list = self.list[:5]

    def add(self, score: Tuple[int, str, int]) -> None:
        """Add score to Scores.list, keeping it sorted.

        :param score: Final score, player name, number of turns
        """
        self.list.append(score)
        self._sort()

    def print(self) -> None:
        """Print styled high scores."""
        print("=" * 40)  # 36 is standard width for menu
        if self.list:
            print("High scores\t\t\tTurns")
            for item in self.list:
                score, name, turns = item
                name_score = f"{name}: {fmt_money(score)}"
                tabs = "\t" if len(name_score) >= 24 else "\t\t"
                print(f"{name_score}{tabs}{turns}")
            print("=" * 40)
        else:
            print("No high scores!")
