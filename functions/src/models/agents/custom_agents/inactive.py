"""Model representing the inactive Pac-Man behaviour"""

from src.models.agents.pacman_agent import PacmanAgent
from src.models.graph import Graph


class InactivePacMan(PacmanAgent):
    """
    Model representing the inactive Pac-Man behaviour.

    In this model, Pac-Man will remain static and not
    move for the entire simulation.
    """

    def __init__(
        self, home_path: list[tuple[int, int]], respawn_point: tuple[int, int]
    ):
        super().__init__(home_path, respawn_point)

    def _perceive(self, time: int, level: Graph) -> None:
        # An inactive Pac-Man does not need to make perceptions.
        pass

    def _execute(self) -> tuple[int, int]:
        # An inactive Pac-Man will always stay in the same place.
        return self.position
