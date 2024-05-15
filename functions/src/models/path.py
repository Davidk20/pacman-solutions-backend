from src.models import pickups
from src.models.environment import EnvironmentEntity
from src.models.node import Node


class Path:
    """
    Model representing a single path.

    This object should be read-only, and acts as a wrapper to allow
    functions to take place on `Path`'s.
    """

    def __init__(self, path: list[Node]) -> None:
        self.route = path

    def __repr__(self) -> str:
        if len(self.route) > 0:
            return f"Path from {self.route[0].position} to {self.route[-1].position}"
        else:
            return "Empty Path"

    def __len__(self) -> int:
        return len(self.route)

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Path) or len(self.route) != len(__value):
            return False
        for a, b in zip(self.route, __value.route):
            if a != b:
                return False
        return True

    def is_safe(self, forward: int = 0) -> bool:
        """
        Checks whether a path is safe.

        Returns
        -------
        `True` if there are no Ghosts on a path.
        """
        iterator = self.route[1:forward] if forward != 0 else self.route[1:]
        for node in iterator:
            # Starts from second index to ignore agent in first position.
            if node.empty():
                continue
            if not node.contains(pickups.Pickup) and not node.contains(
                EnvironmentEntity
            ):
                return False
        return True

    def is_loop(self) -> bool:
        """
        Checks if the path loops on itself.

        Returns
        -------
        `True` if the `Path` starts at the same point that it ends.
        """
        return self.route[0] == self.route[-1]

    def cost(self) -> int:
        """
        Calculates the reward cost of the path.

        This value is seen as the reward for travelling down this path
        and is based on the sum of all score obtained should the agent
        successfully make it to the end of this path.
        """
        score = 0
        for node in self.route:
            if not node.empty():
                if isinstance(node.get_lower_entity(), pickups.Pickup):
                    score += node.get_lower_entity().score()
        return score

    def get_next_pos(self) -> Node:
        """
        Returns the next position to move to and removes this from the queue.

        Returns
        -------
        The `Node` corresponding to the next target position.
        """
        return self.route.pop(0)

    def backwards(self, history: list[tuple[int, int]]) -> bool:
        """
        Check whether the agent would be moving backward's by traversing
        this path.

        Parameters
        ----------
        `history` : `list[tuple[int, int]]`
            The path history of the agent.

        Returns
        -------
        `true` if the agent would be moving backwards down this path.
        """
        if len(history) > 1:
            return self.route[1].position in history[-2:]
        else:
            return False
