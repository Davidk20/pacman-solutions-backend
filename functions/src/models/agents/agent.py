"""
Abstract class used to encapsulate all agent attributes.

Inspiration for this Agent model is being taken from the CS3940 Intelligent
Agents VacuumWorld abstraction. The core functionality of an `Agent` should
follow the agent cycle:

1) Perceive environment state and generate percept through `see()`
2) Revise internal state through `next()`
3) decide which action to select through `action()`
4) Return the action to be executed by the body

https://github.com/dicelab-rhul/vacuumworld
"""

from abc import ABC, abstractmethod

from functions.src.models.entity import Entity
from functions.src.models.graph import Graph
from functions.src.models.movement_types import MovementTypes
from functions.src.models.path import Path
from functions.src.models.position import Position


class Agent(ABC, Entity):
    """Abstract class used to provide core functionality to all agents."""

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
        """
        Initialise the class.

        Parameters
        ----------
        `name` : `str`
            The name of the agent.
        `behaviour` : `str`
            The agents behaviour.
        `movement_type` : `MovementTypes`
            The agent's movement behaviours.
        `home_path` : `list[Position]`
            The agents's home path.
        `value` : `int`
            The agent's representation within the array.
        `score` : `int` : `default = 0`
            The score of the agent. Only ghost agents should override the
            score attribute as they have a score for `Pac-Man` to collect.
        """
        super().__init__(name, score, value)
        self.behaviour = behaviour
        """The agent's behaviour."""
        self.movement_type = movement_type
        """The agents Movement type"""
        self.home_path = home_path
        """The agents's home path."""
        self.position: Position
        """The position of the agent."""
        self.target: list[Position] = []
        """The target path for the agent to follow."""
        self.move_history: list[Position] = []
        """Stores the agents move history."""
        self.respawn_point: Position = respawn_point
        """The point the agent should respawn to."""
        self.path: Path = Path([])
        """The path the agent is following."""

    def __repr__(self) -> str:
        return (
            f"(Name: {self.name}, Score: {self.score}, "
            f"Behaviour: {self.behaviour}, "
            f"Movement: {self.movement_type}), "
            f"Target: {self.target}), "
            f"Position: {self.position}"
        )

    @abstractmethod
    def _perceive(self, time: int, level: Graph) -> None:
        """
        Perceive the environment and generate perceptions.

        Parameters
        ----------
        `state` : `Graph`
            The current state of the game used for decision making.
        """
        raise NotImplementedError

    @abstractmethod
    def _execute(self) -> Position:
        """
        Returns the position which the `Agent` should move to.

        Uses the perceptions and revisions to decide the best action to take.

        Returns
        -------
        A `tuple` containing the coordinates for the agent to move to.
        """
        raise NotImplementedError

    def cycle(self, time: int, level: Graph) -> Position:
        """
        Method encapsulating the entire agent cycle.

        Rather than the GameManager calling each of the stages of the agent cycle,
        this should be hidden from the outside so that only one function is needed
        to allow an agent's decision making.

        Parameters
        ----------
        `state` : `Graph`
            The current state of the game used for decision making.

        Returns
        -------
        A `tuple` containing the coordinates for the agent to move to.
        """
        self._perceive(time, level)
        return self._execute()
