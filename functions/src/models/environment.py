"""Models representing the environment."""

from src.models.entity import Entity


class EnvironmentEntity(Entity):
    """Parent class representing a generic environment entity."""

    def __init__(self, name: str, value: int) -> None:
        """
        Initialise an EnvironmentEntity.

        Parameters
        ----------
        `name` : `str`
            The name of the entity.
        `score` : `int`
            The score the entity has.
        `value` : `int`
            The agent's representation within the array.
        """
        super().__init__(name, 0, value)


class Wall(EnvironmentEntity):
    """Model representing a Wall."""

    def __init__(self) -> None:
        """Initialise the class."""
        super().__init__("Wall", 99)


class Gate(EnvironmentEntity):
    """Model representing the gate between the ghost spawn and the map."""

    def __init__(self) -> None:
        """Initialise the class."""
        super().__init__("Gate", 20)


class Teleporter(EnvironmentEntity):
    """Model representing the gate between teleporter locations."""

    def __init__(self) -> None:
        """Initialise the class."""
        super().__init__("Teleporter", 88)
