"""Model representing a position in two-dimensional space."""

from typing import List


class Position:
    """Model representing a position in two-dimensional space."""

    def __init__(self, x: int, y: int) -> None:
        self._x = x
        """The x-coordinate."""
        self._y = y
        """The y-coordinate."""

    def __repr__(self) -> str:
        return f"(x: {self.x} y: {self.y})"

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Position):
            return self.x == __value.x and self.y == __value.y
        return False

    def __hash__(self) -> int:
        return hash((self._x, self._y))

    @property
    def x(self):
        """The x-coordinate."""
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        """The x-coordinate."""
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    def to_tuple(self) -> tuple[int, int]:
        """Returns the position as a tuple."""
        return (self.x, self.y)

    def add(self, adder: "Position") -> "Position":
        """
        Adds two positions together.

        Parameters
        ----------
        `adder` : `Position`
            The position to add.

        Returns
        -------
        `Position`
            The result of the calculation.
        """
        x = self.x + adder.x
        y = self.y + adder.y
        return Position(x, y)

    def subtract(self, sub: "Position") -> "Position":
        """
        Subtracts one position from another.

        Parameters
        ----------
        `sub` : `Position`
            The position to subtract.

        Returns
        -------
        `Position`
            The result of the calculation.
        """
        x = self.x - sub.x
        y = self.y - sub.y
        return Position(x, y)

    def multiply(self, coefficient: int) -> "Position":
        """
        Multiplies the `Position` by a given coefficient.

        Parameters
        ----------
        `coefficient` : `int`
            The multiplier
        Returns
        -------
        `Position`
            The result of the calculation.
        """
        self.x = self.x * coefficient
        self.y = self.y * coefficient
        return self

    def expand(self) -> List["Position"]:
        """Expands the position in all four axis."""
        return [
            self.add(Position(0, -1)),
            self.add(Position(0, 1)),
            self.add(Position(-1, 0)),
            self.add(Position(1, 0)),
        ]

    def direct_distance(self, other: "Position") -> "Position":
        """
        Returns the positional difference between the two
        """
        return self.subtract(other)

    def euclidean_distance(self, other: "Position") -> float:
        """
        Calculates the distance between this position and the `other` position
        using the Euclidean Distance.

        Parameters
        ----------
        `other` : `Position`
            The other position to calculate the distance to,
            rounded to 4 decimal places.
        """
        return round(((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5, 4)
