"""Collection of models representing the Ghosts."""

from random import choice

from src.models.agents.agent import Agent
from src.models.agents.pacman_agent import PacmanAgent
from src.models.graph import Graph
from src.models.movement_types import MovementTypes
from src.models.path import Path
from src.models.position import Position

# pylint: disable=access-member-before-definition, attribute-defined-outside-init
# looping nature of Agent cycle means access will be before definition
# when defined in previous cycle.


class GhostAgent(Agent):
    """
    Generic agent representing the behaviour of all 4 ghosts.

    Initially, all four ghosts will have the same behaviour and
    therefore can be represented by the same agent. In future
    iterations, they may be evolved to include the subtle differences
    that the ghosts exhibit and so they would be separated into the
    four separate classes again.
    """

    # pylint: disable=too-many-instance-attributes, too-many-arguments
    # attributes required for agent instantiation.

    def __init__(
        self,
        name: str,
        behaviour: str,
        movement_type: MovementTypes,
        home_path: list[Position],
        value: int,
        respawn_point: Position,
        score: int = 0,
    ):
        super().__init__(
            name, behaviour, movement_type, home_path, value, respawn_point, score
        )
        self._internal_time: int = 0
        """
        The ghost's internal clock, not linked to game time.

        The ghost uses an internal timer to time its behaviour changes. This
        is required as, when frightened, the ghosts behaviours stop fluctuating
        between chase and scatter and should return to their pre-frightened
        state after the frightened timer expires
        """
        self.path: Path = Path([])
        """The path the agent is taking."""
        self._frightened_countdown: int = 6

    def _perceive(self, time: int, level: Graph) -> None:  # pylint: disable=W0613
        match self.movement_type:
            case MovementTypes.FRIGHTENED:
                self._frightened_countdown -= 1
                if self._frightened_countdown == 0:
                    # Reset frightened counter
                    self._frightened_countdown = 6
                    self.movement_type = MovementTypes.CHASE

                self.path = choice(level.find_path_to_next_jct(self.position))

            case MovementTypes.SCATTER:
                if len(self.target) > 0 and self.position == self.target[0]:
                    self.target.pop(0)
                self.path = level.shortest_path_to(self.position, self.target[0])

            case MovementTypes.CHASE:
                pacman_node = level.find_node_by_entity(PacmanAgent)[0]
                self.target = [pacman_node.position]
                self.path = level.shortest_path_to(self.position, self.target[0])

            case MovementTypes.CHASE | MovementTypes.SCATTER:
                # Only update time when not frightened
                self._internal_time += 1

                if self._internal_time >= 20 and self._internal_time < 27:
                    self.movement_type = MovementTypes.SCATTER
                    # When scattering to home, this should become their target.
                    self.target = self.home_path
                else:
                    self.movement_type = MovementTypes.CHASE
                    # Reset timer
                    self._internal_time = 0

        if self.movement_type != MovementTypes.HOMEBOUND:
            if self.path.route[0].position == self.position:
                # The path contains the current pos which must be popped from the list
                self.path.get_next_pos()

    def _execute(self) -> Position:
        match self.movement_type:
            case MovementTypes.CHASE | MovementTypes.SCATTER | MovementTypes.FRIGHTENED:
                return self.path.get_next_pos().position
            case _:
                return self.position

    def handle_capture(self) -> None:
        """Handles the event of the ghost being consumed by Pac-Man"""
        self.movement_type = MovementTypes.CHASE


class BlinkyAgent(GhostAgent):
    """
    Specific mind for Blinky the ghost.

    Blinky adapts the generic `Ghost` mind by implementing a
    direct chasing pattern. Blinky will target Pac-Man's exact
    position.
    """

    def __init__(self, homes: list[Position], respawn_point: Position):
        super().__init__(
            "Blinky", "Shadow", MovementTypes.CHASE, homes, 21, respawn_point, 200
        )


class PinkyAgent(GhostAgent):
    """Agent representing the generic logic for Pinky."""

    def __init__(self, homes: list[Position], respawn_point: Position):
        super().__init__(
            "Pinky", "Speedy", MovementTypes.HOMEBOUND, homes, 22, respawn_point, 200
        )

    def _perceive(self, time: int, level: Graph) -> None:
        super()._perceive(time, level)
        # Activate Ghost
        if level.total_pickups - level.remaining_pickups() == 1:
            self.movement_type = MovementTypes.CHASE
            self.path = Path([level.find_node_by_pos(self.respawn_point)])


class InkyAgent(GhostAgent):
    """Agent representing the generic logic for Inky."""

    def __init__(self, homes: list[Position], respawn_point: Position):
        super().__init__(
            "Inky", "Bashful", MovementTypes.HOMEBOUND, homes, 23, respawn_point, 200
        )

    def _perceive(self, time: int, level: Graph) -> None:
        super()._perceive(time, level)
        if level.total_pickups - level.remaining_pickups() == 30:
            self.movement_type = MovementTypes.CHASE
            self.path = Path([level.find_node_by_pos(self.respawn_point)])


class ClydeAgent(GhostAgent):
    """Agent representing the generic logic for Clyde."""

    def __init__(self, homes: list[Position], respawn_point: Position):
        super().__init__(
            "Clyde", "Pokey", MovementTypes.HOMEBOUND, homes, 24, respawn_point, 200
        )

    def _perceive(self, time: int, level: Graph) -> None:
        super()._perceive(time, level)
        if level.total_pickups - level.remaining_pickups() == 60:
            self.movement_type = MovementTypes.CHASE
            self.path = Path([level.find_node_by_pos(self.respawn_point)])
