"""Model representing the randomised Pac-Man behaviour"""

from random import choice

from src.models.agents.pacman_agent import PacmanAgent
from src.models.graph import Graph
from src.models.position import Position


class RandomPacMan(PacmanAgent):
    """
    Model representing the random Pac-Man behaviour.

    In this model, Pac-Man will randomly choose a path. I have chosen to
    implement this behaviour similar to that of a frightened ghost.
    Pac-Man will randomly choose a new direction at each junction.
    """

    def __init__(self, home_path: list[Position], respawn_point: Position):
        super().__init__(home_path, respawn_point)

    def _perceive(self, time: int, level: Graph) -> None:
        current_node = level.find_node_by_pos(self.position)

        # If the current path is valid then stay on this path
        if not level.is_junction(current_node) and len(self.path) > 0:
            return

        all_paths = level.find_path_to_next_jct(self.position)
        # prune paths where the path only contains the target.
        valid_paths = [path for path in all_paths if len(path) > 2]
        if len(self.move_history) > 2:
            # Remove any paths which would take the agent backwards
            valid_paths = [
                path
                for path in valid_paths
                if path.route[1].position != self.move_history[-2]
            ]
        self.path = choice(valid_paths)
        if self.path.route[0].position == self.position:
            # if the path contains the current pos it must be removed from the list
            self.path.get_next_pos()

    def _execute(self) -> Position:
        move = self.path.get_next_pos().position
        self.move_history.append(move)
        return move
