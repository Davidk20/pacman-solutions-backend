from src.models.agents.pacman_agent import PacmanAgent
from src.models.graph import Graph
from src.models.path import Path


class GreedyPacMan(PacmanAgent):
    """
    Model representing the greedy Pac-Man behaviour.

    In this model, Pac-Man will always choose the highest scoring move,
    regardless of length or ghost presence. The only pruning that should
    take place is to remove any game-breaking paths such as stationary routes.
    """

    def __init__(
        self, home_path: list[tuple[int, int]], respawn_point: tuple[int, int]
    ):
        super().__init__(home_path, respawn_point)

    def _perceive(self, time: int, level: Graph) -> None:
        # Get all paths to next jct
        paths = level.find_path_to_next_jct(self.position)
        paths = [path for path in paths if not path.is_loop()]
        sorted_paths = sorted(paths, key=lambda path: path.cost(), reverse=True)
        self.path: Path = sorted_paths[0]
        # remove current pos from path to prevent static glitch
        self.path.get_next_pos()

    def _execute(self) -> tuple[int, int]:
        move = self.path.get_next_pos().position
        self.move_history.append(move)
        return move
