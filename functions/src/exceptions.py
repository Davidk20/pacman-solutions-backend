"""Centralised file for all exceptions."""

##########################################
#            Game Exceptions
##########################################


class PacManDiedException(Exception):
    """Raised when Pac-Man dies."""

    def __init__(self) -> None:
        super().__init__()


class GhostDiedException(Exception):
    """Raised when a ghost is consumed."""

    def __init__(self, ghost) -> None:
        """
        Exception raised when a ghost is consumed.

        Parameters
        ----------
        `ghost` : `GhostAgent`
            The ghost which has been consumed.
        `pos` : `Position`
            The position they must return to.
        """
        super().__init__()
        self.ghost = ghost


##########################################
#            Level Exceptions
##########################################


class LevelNotFoundException(Exception):
    """Raised when a level is not found."""

    def __init__(self, level_num: int) -> None:
        super().__init__(f"Level {level_num} not found.")


class InvalidLevelConfigurationException(Exception):
    """Raised when a level is not configured correctly."""

    def __init__(self, level_num: int) -> None:
        super().__init__(f"Level {level_num} is not configured correctly.")


##########################################
#            Node Exceptions
##########################################
class InvalidNodeException(Exception):
    """Raised when a queried Node cannot be found."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


##########################################
#            Graph Exceptions
##########################################
class NodeNotFoundException(Exception):
    """Raised when a queried Node cannot be found."""

    def __init__(self, pos: tuple[int, int]) -> None:
        super().__init__(f"Node not found at {pos}.")


class PathNotFoundException(Exception):
    """Raised when a path cannot be found."""

    def __init__(self, pos: tuple[int, int]) -> None:
        super().__init__(f"Path not found from {pos}")


class DuplicateNodeException(Exception):
    """Raised when it is attempted to add a repeated node."""

    def __init__(self, node: str) -> None:
        super().__init__(f"{node} already in graph.")


class InvalidGraphConfigurationException(Exception):
    """Raised when the graph does not fit the required configuration."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class CollisionException(Exception):
    """Raised when there is a collision between agents."""

    def __init__(self, colliding_node) -> None:
        """
        Exception raised when an agent collides with an entity.

        Parameters
        ----------
        `colliding_node` : `Agent`
            The agent which is moving
        """
        self.node = colliding_node
        self.agent = colliding_node.get_higher_entity()
        self.colliding_entity = colliding_node.get_lower_entity()
        super().__init__(
            f"{self.agent.name()} collided with {self.colliding_entity.name()}"
            f" at {self.node.position}"
        )
