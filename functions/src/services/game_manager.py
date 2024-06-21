"""Service managing the running of the game."""

from enum import Enum

from src import exceptions
from src.models.agents import ghost_agent
from src.models.agents.custom_agents.adventurous import AdventurousPacMan
from src.models.agents.pacman_agent import PacmanAgent
from src.models.agents.placeholder_agent import PlaceholderAgent
from src.models.game_state import GameState
from src.models.game_state_store import GameStateStore
from src.models.graph import Graph
from src.services import level_handler
from src.utils import game_utils, level_utils


class RunConfiguration(Enum):
    """Representation of the run type for `GameManager`."""

    LOCAL = "local"
    SERVER = "server"
    ANALYTIC = "analytic"


class GameManager:
    """
    Service which manages the overall running of the game.
    """

    # pylint: disable=too-many-instance-attributes
    # Nine required for game instantiation.

    def __init__(
        self,
        level_num: int,
        configuration: RunConfiguration,
        custom_pacman: type[PacmanAgent] = AdventurousPacMan,
        verbose: bool = False,
    ) -> None:
        """
        Initialises the `GameManager`.

        The game manager is responsible for building the game with all requirements
        and then running the game, managing its iteration and win / loss conditions.

        There are two run configurations: `local` and `server`. If `GameManager`
        is run locally, this refers to it being run using the
        `if __name__ == "__main__"` call. In this case, the outputs of simulations
        should be printed to the terminal. If `GameManager` is being run by the
        server then all output should be returned so that it can be passed back
        in server messages.

        Parameters
        ----------
        `level_num` : `int`
            The number of the level to be run.
        `configuration` : `RunConfiguration`
            The configuration used for the run.
        `custom_pacman` : `type[PacmanAgent]`
            The custom agent to be injected into the game.
            The default is `InformedPacMan`.
        `local` : `bool` DEFAULT = `False`
            Whether the game is being run locally or as a server call. Used to
            indicate whether output should be printed or not.
        `verbose` : `bool` DEFAULT = `False`
            If `True`, the verbose output will be displayed
        """
        self.configuration: RunConfiguration = configuration
        """The configuration used for the model run."""
        self.verbose: bool = verbose
        """Indicates whether to display the verbose output."""
        self.timer = 0
        """
        The internal game counter.

        A unit of time is interpreted as the duration it takes any agent to
        move one space anywhere on the board. This way, all movements take
        the same duration of time and can be counted within the same unit and
        the planner does not have to worry about moves being completed at
        different times and then having to factor this into collision
        calculations.
        """
        self.state_store = GameStateStore()
        """The store containing the history of the agents movements."""
        self.game: Graph = level_utils.array_to_graph(level_handler.get_map(level_num))
        """The graph containing the game."""
        self.running = False
        """Indicates whether the game is currently running."""
        agent_home = level_handler.get_homes(level_num)
        """Dictionary containing the homes of the agents."""
        self.respawn = level_handler.get_respawn_points(level_num)
        """Dictionary containing the agents respawn points."""
        self.pacman = custom_pacman(agent_home["pacman"], self.respawn["pacman"])
        """Representation of the Pac-Man agent."""
        self.agents: list[PacmanAgent | ghost_agent.GhostAgent] = [
            self.pacman,
            ghost_agent.BlinkyAgent(agent_home["blinky"], self.respawn["blinky"]),
            ghost_agent.PinkyAgent(agent_home["pinky"], self.respawn["pinky"]),
            ghost_agent.InkyAgent(agent_home["inky"], self.respawn["inky"]),
            ghost_agent.ClydeAgent(agent_home["clyde"], self.respawn["clyde"]),
        ]
        """Array containing all of the agents."""

    def setup_game(self) -> None:
        """
        Setup the game and board before the game starts.

        Injects the populated agents into the place of the dummy agents.
        """
        for placeholder in self.game.find_node_by_entity(PlaceholderAgent):
            for ag in self.agents:
                if placeholder.get_higher_entity().value() == ag.value():
                    placeholder.remove_entity(placeholder.get_higher_entity())
                    placeholder.add_entity(ag)
                    break

    def win(self) -> bool:
        """
        Checks whether the conditions for a win have been met.

        Returns
        -------
        `True` if the game is won and `False` otherwise.
        """
        return self.game.remaining_pickups() == 0

    def lost(self) -> bool:
        """
        Checks whether the conditions for a loss have been met.

        Returns
        -------
        `True` if the game is lost and `False` otherwise.
        """
        return self.pacman.current_lives == 0

    def tick(self) -> None:
        """Increments the game time and processes all time based events."""
        level_array = level_utils.graph_to_array(self.game)
        self.state_store.add(
            GameState(
                self.timer, level_array, self.pacman.energized, self.pacman.score()
            )
        )
        if self.win() or self.lost():
            self.running = False
        else:
            self.timer += 1
        self.pacman.handle_energised()
        for ag in self.agents:
            try:
                ag.position = self.game.find_node_by_entity(type(ag))[0].position
                self.game.move_agent(
                    ag.position, ag.cycle(self.timer, self.game), type(ag)
                )
            except exceptions.CollisionException as collision:
                try:
                    game_utils.handle_collision(collision.node)
                except exceptions.PacManDiedException:
                    self.running = False
                except exceptions.GhostDiedException as ghost:
                    if isinstance(ghost.ghost, ghost_agent.GhostAgent):
                        ghost.ghost.handle_capture()
                        self.game.move_agent(
                            collision.node.position,
                            self.respawn[ghost.ghost.name().lower()],
                            ghost_agent.GhostAgent,
                        )
            except IndexError as e:
                print(f"{ag} - {e}")
                self.running = False
                raise

    def game_loop(self) -> dict:
        """
        Start the game loop.

        Returns
        -------
        `GameStateStore`
            The history of moves
        """
        self.setup_game()
        self.running = True
        while self.running:
            try:
                self.tick()
            except KeyboardInterrupt:
                print("\nSimulation manually stopped")
                break
        # append final state after game ended
        self.state_store.add(
            GameState(
                self.timer,
                level_utils.graph_to_array(self.game),
                self.pacman.energized,
                self.pacman.score(),
            )
        )
        return self.handle_end()

    def print_current_state(self) -> None:
        """
        Print the latest state of the game.

        Used for debugging and should only be called when an exception is caught.
        """
        print(f"Iteration {self.timer}")
        print(level_utils.print_level(level_utils.graph_to_array(self.game)))

    def handle_end(self, ghost: ghost_agent.GhostAgent = None) -> dict:  # type: ignore
        """
        Handles the end of the game.

        Parameters
        ----------
        `ghost` : `GhostAgent`
            The ghost which defeated Pac-Man - if applicable.
        """

        match self.configuration:
            case RunConfiguration.LOCAL:
                print("##############################")
                print("GAME OVER")
                print("##############################")
                print(f"Time: {self.timer}")
                print(f"Pac-Man score: {self.pacman.score()}")
                if ghost:
                    print(f"{ghost.name()} caught Pac-Man at {self.pacman.position}")
                if self.verbose:
                    self.print_current_state()
                return self.state_store.to_json()

            case RunConfiguration.SERVER:
                return self.state_store.to_json()

            case RunConfiguration.ANALYTIC:
                return {"time_game": self.timer, "score": self.pacman.score()}
