"""Model representing the agent for Pac-man."""

from functions.src import exceptions
from functions.src.models.agents.agent import Agent
from functions.src.models.graph import Graph
from functions.src.models.movement_types import MovementTypes
from functions.src.models.pickups import Pickup, PowerPellet
from functions.src.models.position import Position


class PacmanAgent(Agent):
    """
    Model representing the agent for Pac-man.

    This class should be used as a wrapper for all implementations
    of the Pac-Man model. This class will provide all of the generic
    game logic which prevents the need for this to be implemented in
    each interpretation of the PacmanAgent.

    Inspirations for Pac-Man decision making comes from the below
    sources:
    https://github.com/Lamonkey/ai-pacman
    https://www.classicgaming.cc/classics/pac-man/play-guide
    """

    def __init__(self, home_path: list[Position], respawn_point: Position):
        """
        Initialise the class.

        Parameters
        ----------
        `home_path` : `list[Position]`
            The agents's home path.
        """
        super().__init__(
            "Pac-Man", "Player", MovementTypes.CUSTOM, home_path, 44, respawn_point
        )
        self.current_lives = 1
        """Store the number of lives the user agent has remaining."""
        self.energized = False
        """
        Store whether Pac-man is currently energized. This is true when the
        agent has consumed a Power Pellet and is then able to consume ghosts.
        """
        self.temp_ghost_counter = 0
        """
        Counter to store the number of ghosts that Pac-man has consumed during
        a single energizer run
        """
        self.time_since_energised = 0

    def __repr__(self) -> str:
        return (
            f"(Name: {self.name}, Score: {self.score}, "  # pylint: disable=E1101
            f"Lives: {self.current_lives}, Energized: {self.energized}, "
            f"Ghosts Consumed: {self.temp_ghost_counter}), "
            f"Position: {self.position}"
        )

    def increase_score(self, score: int) -> None:
        """
        Increase the agents score.

        Parameters
        ----------
        `score` : `int`
            The amount of score to increase the Pac-Man's score by.
        """
        self.score += score  # pylint: disable=E1101

    def handle_consume(self, pickup: Pickup | Agent):
        """
        Handle the logic behind Pac-man consuming an item.

        :param pickup: The Pickup they have consumed.
        """
        if isinstance(pickup, PowerPellet):
            self.energized = True
        if isinstance(pickup, Agent):
            if not self.energized:
                # If Pac-man has consumed a ghost without energizer
                self.current_lives -= 1
                raise exceptions.PacManDiedException()

            # If Pac-man has successfully consumed a ghost
            self.temp_ghost_counter += 1
            score = int(((pickup.score / 100) ** self.temp_ghost_counter) * 100)
            self.increase_score(score)
            raise exceptions.GhostDiedException(pickup)

        if not isinstance(pickup, Agent):
            self.increase_score(pickup.score)

    def handle_energised(self):
        """Handles the logic surrounding Pac-Man's energised state."""
        if not self.energized:
            return
        if self.time_since_energised == 7:
            self.deenergize()
        self.time_since_energised += 1

    def deenergize(self):
        """Restore Pac-man agent to a de-energized state."""
        self.energized = False
        self.temp_ghost_counter = 0
        self.time_since_energised = 0

    def _perceive(self, time: int, level: Graph) -> None:
        raise NotImplementedError

    def _execute(self) -> Position:
        raise NotImplementedError
