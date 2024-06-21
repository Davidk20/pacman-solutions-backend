"""Model representing the Greedy Pac-Man behaviour."""

import random

from functions.src.models.agents.pacman_agent import PacmanAgent
from functions.src.models.graph import Graph
from functions.src.models.position import Position


class GreedyPacMan(PacmanAgent):
    """
    Model representing the greedy Pac-Man behaviour.

    In this model, Pac-Man will always choose the highest scoring move,
    regardless of length or ghost presence. The only pruning that should
    take place is to remove any game-breaking paths such as stationary routes.
    """

    # pylint: disable=access-member-before-definition, attribute-defined-outside-init
    # looping nature of Agent cycle means access will be before definition
    # when defined in previous cycle.

    def _perceive(self, level: Graph) -> None:
        current_node = level.find_node_by_pos(self.position)
        # If the current path is valid then stay on this path
        if not level.is_junction(current_node) and len(self.path) > 0:
            return
        # Get all paths to next jct
        paths = level.find_path_to_next_jct(self.position)
        max_cost = max(path.cost() for path in paths)
        max_cost_paths = [path for path in paths if path.cost() == max_cost]
        self.path = random.choice(max_cost_paths)
        # remove current pos from path to prevent static glitch
        self.path.get_next_pos()

    def _execute(self) -> Position:
        move = self.path.get_next_pos().position
        self.move_history.append(move)
        return move
