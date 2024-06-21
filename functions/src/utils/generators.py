"""Generate instances for top-level services"""

from src.models.agents.custom_agents.adventurous import AdventurousPacMan
from src.models.agents.custom_agents.greedy import GreedyPacMan
from src.models.agents.custom_agents.inactive import InactivePacMan
from src.models.agents.custom_agents.informed import InformedPacMan
from src.models.agents.custom_agents.unplanned import UnplannedPacMan
from src.models.agents.pacman_agent import PacmanAgent


def gen_agent(agent: str = "") -> type[PacmanAgent]:
    """
    Generates an agent instance from a string.

    Parameters
    ----------
    `agent` : `str`
        The name of the agent to return

    Returns
    -------
    The `type` of the queried agent.
    """
    match agent.lower():
        case "adventurous":
            return AdventurousPacMan
        case "greedy":
            return GreedyPacMan
        case "inactive":
            return InactivePacMan
        case "informed":
            return InformedPacMan
        case "unplanned":
            return UnplannedPacMan
        case _:
            raise ValueError(f"Agent {agent} not found.")
