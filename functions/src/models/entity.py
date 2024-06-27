"""Model representing all entities within the game."""

from dataclasses import dataclass


@dataclass
class Entity:
    """Model representing all entities within the game."""

    name: str
    """The name of the entity."""
    score: int = 0
    """The score the entity has."""
    value: int = 999
    """The agent's representation within the array."""

    def __repr__(self) -> str:
        return f"""(Name: {self.name}, Score: {self.score}, Value: {self.value})"""

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Entity):  # pylint: disable=W0143
            return False
        return self.name == __value.name and self.value == __value.value
