"""Collection of objects representing the pickups possible during gameplay."""

from src.models.entity import Entity


class Pickup(Entity):
    """Parent class representing a generic Pickup item."""


class Empty(Pickup):
    """`Pickup` class representing an empty space."""

    def __init__(self) -> None:
        """Initialise the class."""
        super().__init__("Empty", 0, 0)


class PacDot(Pickup):
    """Pickup class representing a standard Pac-Dot."""

    def __init__(self) -> None:
        """Initialise the class."""
        super().__init__("PacDot", 10, 1)


class PowerPellet(Pickup):
    """Pickup class representing a Power Pellet, also known as an Energizer."""

    def __init__(self) -> None:
        """Initialise the class."""
        super().__init__("Power Pellet", 50, 2)


class Cherry(Pickup):
    """Pickup class representing a Cherry."""

    def __init__(self) -> None:
        """Initialise the class."""
        super().__init__("Cherry", 100, 3)


class Strawberry(Pickup):
    """Pickup class representing a Strawberry."""

    def __init__(self) -> None:
        """Initialise the class."""
        super().__init__("Strawberry", 300, 4)


class Orange(Pickup):
    """Pickup class representing a Orange."""

    def __init__(self) -> None:
        """Initialise the class."""
        super().__init__("Orange", 500, 5)


class Apple(Pickup):
    """Pickup class representing a Apple."""

    def __init__(self) -> None:
        """Initialise the class."""
        super().__init__("Apple", 700, 6)


class Melon(Pickup):
    """Pickup class representing a Melon."""

    def __init__(self) -> None:
        """Initialise the class."""
        super().__init__("Melon", 1000, 7)


class Galaxian(Pickup):
    """Pickup class representing a Galaxian."""

    def __init__(self) -> None:
        """Initialise the class."""
        super().__init__("Galaxian", 2000, 8)


class Bell(Pickup):
    """Pickup class representing a Bell."""

    def __init__(self) -> None:
        """Initialise the class."""
        super().__init__("Bell", 3000, 9)


class Key(Pickup):
    """Pickup class representing a Key."""

    def __init__(self) -> None:
        """Initialise the class."""
        super().__init__("Key", 5000, 10)
