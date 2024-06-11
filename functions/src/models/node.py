"""Model representing a node within a graph."""

from typing import Type, TypeVar

from src.models.entity import Entity
from src.models.pickups import Empty, Pickup

from src import exceptions


class Node:
    """
    Model representing a node within a graph.

    As well as storing itself and connected nodes, the nodes will be used to
    encode positional data about the position of the node relative to the level
    as well as what items or agents are currently in that position.
    """

    T = TypeVar("T")

    def __init__(self, position: tuple[int, int], starting_entity: Entity) -> None:
        """
        Initialise a `Node` object.

        Parameters
        ----------
        `position` : `tuple[int, int]`
            Tuple containing the x and y coordinates of
            the node relative to the array.

        `entity` : `Entity`
            The entity which is currently in this space.
        """
        self.visited = False
        """`true` if the node has been visited by the Pac-Man agent."""
        self.position = position
        """The position of the node in relation to the array-based level."""
        self.entities: list[Entity] = (
            [starting_entity] if not isinstance(starting_entity, Empty) else []
        )
        """
        Stores the entities currently within this space.

        Only one entity should be passed in as there should only be one entity per
        space at the start of the game.
        """

    def __repr__(self) -> str:
        entities = [entity.name() for entity in self.entities]
        return f"""\nPosition: {self.position}, Contains: {entities}"""

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Node):
            return self.position == __value.position
        return False

    def __hash__(self) -> int:
        return hash(self.position)

    def empty(self) -> bool:
        """Returns `True` if the `Node` is empty."""
        return len(self.entities) == 0

    def is_collision(self) -> bool:
        """Returns `True` if there is a collision in this `Node`."""
        return len(self.entities) >= 2

    def contains(self, entity_type: Type[Entity]) -> bool:
        """Returns `True` if the `Node` contains an entity of the provided type."""
        return any(isinstance(entity, entity_type) for entity in self.entities)

    def add_entity(self, entity: Entity) -> None:
        """
        Adds an entity to the `Node`.

        Parameters
        ----------
        `entity` : `Entity`
            The entity to add to the `Node`.
        """
        if isinstance(entity, Pickup) and self.contains(Pickup):
            raise exceptions.InvalidNodeException("Cannot have two pickups in one node")
        self.entities.append(entity)

    def remove_entity(self, entity: Entity) -> None:
        """
        Removes a given entity from the `Node`.

        Parameters
        ----------
        `entity` : `Entity`
            The entity to remove from the `Node`.
        """
        try:
            self.entities.remove(entity)
        except ValueError:
            raise exceptions.InvalidNodeException(f"Cannot remove {entity.name()}")

    def get_higher_entity(self) -> Entity:
        """
        Returns the 'highest priority' entity from the `Node`.

        Returns
        -------
        The highest priority entity. This will be an `Agent` if there is an `Agent`
        in the `Node`, otherwise it will be a `Pickup`. If the `Node` is empty
        then it will return `Empty`. If the `Node` contains two `Agent`'s, then the
        higher priority `Node` should be the most recently added `Agent`.
        """
        if self.empty():
            return Empty()
        if len(self.entities) == 1:
            return self.entities[0]
        if isinstance(self.entities[0], Pickup):
            return self.entities[1]
        if not isinstance(self.entities[0], Pickup) and not isinstance(
            self.entities[1], Pickup
        ):
            return self.entities[1]
        return self.entities[-1]

    def get_lower_entity(self) -> Entity:
        """
        Returns the 'lowest priority' entity from the `Node`.

        Returns
        -------
        The lowest priority entity. If there is a `Pickup` then this will be
        returned otherwise it will return an `Agent`. If the `Node` contains
        two `Agent`'s, then the lower priority `Node` should be the first
        added `Agent`.
        """
        if self.empty():
            return Empty()
        if len(self.entities) == 1:
            return self.entities[0]
        if isinstance(self.entities[0], Pickup):
            return self.entities[0]
        if not isinstance(self.entities[0], Pickup) and not isinstance(
            self.entities[1], Pickup
        ):
            return self.entities[0]
        return self.entities[0]

    def get_entity(self, entity_type: Type[T]) -> T:
        """
        Returns an entity
        """
        for entity in self.entities:
            if isinstance(entity, entity_type):
                return entity
        raise exceptions.InvalidNodeException(
            f"Entity of type {entity_type} not found."
        )
