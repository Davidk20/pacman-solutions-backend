from random import choice

from src.models.agents.pacman_agent import PacmanAgent
from src.models.graph import Graph
from src.models.path import Path
from src.models.position import Position


class InformedPacMan(PacmanAgent):
    """
    Model representing the informed random Pac-Man behaviour.

    In this model, Pac-Man will randomly choose a path, however,
    should he reach an unsafe path, Pac-Man will randomly
    choose a new position as target.
    """

    def __init__(self, home_path: list[Position], respawn_point: Position):
        super().__init__(home_path, respawn_point)

    def _perceive(self, time: int, level: Graph) -> None:
        current_node = level.find_node_by_pos(self.position)
        if (
            not level.is_junction(current_node)
            and len(self.path) > 0
            and self.path.is_safe()
        ):
            return

        # Get all paths to next jct
        paths = level.find_path_to_next_jct(self.position)
        # Find all safe paths
        valid_paths: list[Path] = [path for path in paths if path.is_safe()]
        # prune paths where the path only contains the target.
        valid_paths = [path for path in valid_paths if len(paths) > 2]
        # prune paths where the end point == starting point
        valid_paths = [path for path in valid_paths if not path.is_loop()]
        backwards_paths = valid_paths
        if len(self.move_history) > 2:
            # Remove any paths which would take the agent backwards
            valid_paths = [
                path
                for path in valid_paths
                if path.route[1].position != self.move_history[-2]
            ]

        # choose a safe path to follow
        if len(valid_paths) > 0:
            sorted_paths = sorted(
                valid_paths, key=lambda path: path.cost(), reverse=True
            )
            self.path: Path = sorted_paths[0]
        # If no safe paths exist, allow backwards paths.
        elif len(backwards_paths) > 0:
            self.path = choice(backwards_paths)
        else:
            # If no safe path is found, choose the best scoring path
            # so that highest score can be obtained before death.
            self.path = max(paths, key=lambda path: path.cost())
        # remove current pos from path to prevent static glitch
        self.path.get_next_pos()

    def _execute(self) -> Position:
        move = self.path.get_next_pos().position
        self.move_history.append(move)
        return move
