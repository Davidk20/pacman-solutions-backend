"""Model representing all entities within the game."""


class Entity:
    def __init__(self, name: str, score: int = 0, value: int = 999) -> None:
        """
        Initialise an Entity.

        Parameters
        ----------
        `name` : `str`
            The name of the entity.
        `score` : `int`
            The score the entity has.
        `value` : `int`
            The agent's representation within the array.
        """
        self._name = name
        """The name of the entity."""
        self._score = score
        """The score the entity has."""
        self._value = value
        """The agent's representation within the array."""

    def __repr__(self) -> str:
        return f"""(Name: {self._name}, Score: {self._score}, Value: {self._value})"""

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Entity):
            return False
        return self.name == __value.name() and self._value == __value.value()

    def name(self) -> str:
        """Return the entities name."""
        return self._name

    def score(self) -> int:
        """Return the entities score."""
        return self._score

    def value(self) -> int:
        """Return the entities name."""
        return self._value
