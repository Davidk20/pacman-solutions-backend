"""Model representing a position in two-dimensional space."""


class Position:
    """Model representing a position in two-dimensional space."""

    def __init__(self, x: int, y: int) -> None:
        self._x = x
        """The x-coordinate."""
        self._y = y
        """The y-coordinate."""

    def __repr__(self) -> str:
        return f"x: {self.x} y: {self.y}"

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Position):
            return self.x == __value.x and self.y == __value.y
        else:
            return False

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
        self.x += adder.x
        self.y += adder.y
        return self

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
        self.x -= sub.x
        self.y -= sub.y
        return self

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
