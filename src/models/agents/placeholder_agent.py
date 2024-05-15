from src.models.agents.agent import Agent
from src.models.movement_types import MovementTypes


class PlaceholderAgent(Agent):
    """
    A placeholder instance of `Agent`.

    The placeholder is designed to be used during the conversion from an array
    to a graph. During this process, the graph needs Agents to be inserted, however,
    the intelligent agents are not yet configured and so these placeholders will
    sit in their place. They are still given the name and value attributes as they are
    useful during debugging and output. This agent should NEVER be left in a running
    simulation and is only used to allow the initial conversion to take place
    successfully.
    """

    def __init__(self, name: str, value: int):
        super().__init__(name, "", MovementTypes.CUSTOM, [], value, 200)

    def _perceive(self, time: int, level: list[list[int]]) -> None:
        raise NotImplementedError

    def _execute(self) -> tuple[int, int]:
        raise NotImplementedError
