from src.models import environment
from src.models.agents.ghost_agent import GhostAgent
from src.models.agents.pacman_agent import PacmanAgent
from src.models.graph import Graph
from src.models.movement_types import MovementTypes
from src.models.path import Path


class AuthenticPinky(GhostAgent):
    """Represents a game-authentic version of Pinky."""

    def __init__(self, homes: list[tuple[int, int]]):
        super().__init__("Pinky", "Speedy", MovementTypes.HOMEBOUND, homes, 22, 200)

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
            diff = (
                (pacman.position[0] - pacman.move_history[-1][0]),
                (pacman.position[1] - pacman.move_history[-1][1]),
            )
            self.target = [
                (pacman.position[0] + (diff[0] * 4), pacman.position[1] + (diff[1] * 4))
            ]
            self.path = level.shortest_path_to(self.position, self.target[0])
            if self.path.route[0].position == self.position:
                # The path contains the current pos which must be popped from the list
                self.path.get_next_pos()
