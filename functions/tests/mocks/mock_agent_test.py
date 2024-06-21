"""Mock values for agents."""

from functions.src.models.agents.ghost_agent import GhostAgent
from functions.src.models.movement_types import MovementTypes


def mock_ghost() -> GhostAgent:
    """Generate a mock ghost."""
    return GhostAgent("Blinky", "", MovementTypes.CHASE, [], 21, (0, 0), 200)


def mock_ghosts() -> list[GhostAgent]:
    """Generate a mock of all of the ghosts."""
    return [
        GhostAgent("Blinky", "", MovementTypes.CHASE, [], 21, (0, 0), 200),
        GhostAgent("Pinky", "", MovementTypes.CHASE, [], 22, (0, 0), 200),
        GhostAgent("Inky", "", MovementTypes.CHASE, [], 23, (0, 0), 200),
        GhostAgent("Clyde", "", MovementTypes.CHASE, [], 24, (0, 0), 200),
    ]
