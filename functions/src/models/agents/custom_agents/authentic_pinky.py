"""Agent representing a game-authentic version of Pinky."""

from functions.src.models import environment
from functions.src.models.agents.ghost_agent import GhostAgent
from functions.src.models.agents.pacman_agent import PacmanAgent
from functions.src.models.graph import Graph
from functions.src.models.movement_types import MovementTypes
from functions.src.models.path import Path
from functions.src.models.position import Position


class AuthenticPinky(GhostAgent):
    """Represents a game-authentic version of Pinky."""

    # pylint: disable=access-member-before-definition, attribute-defined-outside-init
    # looping nature of Agent cycle means access will be before definition
    # when defined in previous cycle.

    def __init__(self, homes: list[Position]):
        super().__init__(
            "Pinky", "Speedy", MovementTypes.HOMEBOUND, homes, 22, Position(1, 1), 200
        )

    def _perceive(self, time: int, level: Graph) -> None:
        super()._perceive(time, level)
        # Activate Ghost
        if level.total_pickups - level.remaining_pickups() == 1:
            self.movement_type = MovementTypes.CHASE
            self.path = Path([level.find_node_by_entity(environment.Gate)[0]])

        if self.movement_type == MovementTypes.CHASE:
            pacman_node = level.find_node_by_entity(PacmanAgent)[0]
            # calculate Pac-Man's direction
            pacman: PacmanAgent = pacman_node.get_entity(PacmanAgent)
            diff = pacman.position.subtract(pacman.move_history[-1])
            self.target = [
                Position(
                    pacman.position.x + (diff.x * 4), pacman.position.y + (diff.y * 4)
                )
            ]
            self.path = level.shortest_path_to(self.position, self.target[0])
            if self.path.route[0].position == self.position:
                # The path contains the current pos which must be popped from the list
                self.path.get_next_pos()
