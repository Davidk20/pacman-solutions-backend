"""Agent representing the Adventurous Pac-Man."""

import random

from src.models.agents.pacman_agent import PacmanAgent
from src.models.graph import Graph
from src.models.path import Path
from src.models.position import Position


class AdventurousPacMan(PacmanAgent):
    """
    Model representing the Adventurous Pac-Man behaviour.

    In this model, Pac-Man will always choose the longest path. Before choosing
    the longest path, pruning takes place to remove any invalid or unsafe paths.
    """

    # pylint: disable=access-member-before-definition, attribute-defined-outside-init
    # looping nature of Agent cycle means access will be before definition
    # when defined in previous cycle.

    def _perceive(self, time: int, level: Graph) -> None:  # pylint: disable=W0613
        current_node = level.find_node_by_pos(self.position)
        # If the current path is valid then stay on this path
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
        longest = max(len(path) for path in valid_paths)
        longest_paths = [path for path in valid_paths if len(path) == longest]
        self.path = random.choice(longest_paths)
        # remove current pos from path to prevent static glitch
        self.path.get_next_pos()

    def _execute(self) -> Position:
        move = self.path.get_next_pos().position
        self.move_history.append(move)
        return move
