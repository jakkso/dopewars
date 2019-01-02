"""
Holds Scores class
"""
import csv
from typing import List, Tuple

from dopewars.utilities import fmt_money


class Scores:
    """
    Manages storing and retrieving scores to disk.
    Given that this is run as a docker container, relies
    on a volume being supplied to the `docker run` command
    """

    def __init__(self, file: str = "/app/scores.csv") -> None:
        self._file = file
        self.list: List[Tuple[int, str]] = None
        self._read()

    def __str__(self) -> str:
        return f"{self.__class__.__name__}"

    def save(self) -> None:
        """
        Sorts list, writes top five scores to disk
        """
        self.sort()
        with open(self._file, "w", newline="") as file:
            writer = csv.writer(file, delimiter=" ", quotechar="|")
            for score in self.list:
                writer.writerow(score)

    def _read(self) -> None:
        """
        Reads file, converts to machine-usable data
        """
        try:
            with open(self._file, "r", newline="") as file:
                reader = csv.reader(file, delimiter=" ", quotechar="|")
                self.list = [tuple((int(row[0]), row[1])) for row in reader]
        except FileNotFoundError:
            self.list = []

    def sort(self) -> None:
        """
        Sorts list by value of the 0th element of each tuple, trims list to
        len of 5
        """
        self.list.sort(key=lambda item: item[0], reverse=True)
        if len(self.list) > 5:
            self.list = self.list[:5]

    def add(self, score: Tuple[int, str]) -> None:
        """
        Adds score to Scores.list, keeping it sorted
        :param score:
        :return:
        """
        self.list.append(score)
        self.sort()

    def print(self) -> None:
        """
        Prints out styled high scores
        """
        print("=" * 36)  # 36 is standard width for menu
        if self.list:
            print("High scores")
            for item in self.list:
                score, name = item
                print(f"{name}: ${fmt_money(score)}")
            print("=" * 36)
        else:
            print("No high scores!")
