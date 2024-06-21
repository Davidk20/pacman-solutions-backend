"""Utility functions serving the Entity models."""

from src.models import environment, pickups
from src.models.agents import agent
from src.models.agents.placeholder_agent import PlaceholderAgent


class EntityNotFoundException(Exception):
    """Raised when a queried entity cannot be found."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


def convert_value_to_entity(
    value: int,
) -> pickups.Pickup | agent.Agent | environment.EnvironmentEntity:
    """
    Convert a numerical value into a game entity.

    Parameters
    ----------
    `value` : `int`
        The value taken from the array.

    Returns
    -------
    The entity corresponding to the value.
    """

    # pylint: disable=too-many-return-statements
    # Switch statement needed for this many game items.

    match value:
        case 0:
            return pickups.Empty()
        case 1:
            return pickups.PacDot()
        case 2:
            return pickups.PowerPellet()
        case 3:
            return pickups.Cherry()
        case 4:
            return pickups.Strawberry()
        case 5:
            return pickups.Orange()
        case 6:
            return pickups.Apple()
        case 7:
            return pickups.Melon()
        case 8:
            return pickups.Galaxian()
        case 9:
            return pickups.Bell()
        case 10:
            return pickups.Key()
        case 20:
            return environment.Gate()
        case 21:
            return PlaceholderAgent("Blinky", 21)
        case 22:
            return PlaceholderAgent("Pinky", 22)
        case 23:
            return PlaceholderAgent("Inky", 23)
        case 24:
            return PlaceholderAgent("Clyde", 24)
        case 44:
            return PlaceholderAgent("Pacman", 44)
        case 88:
            return environment.Teleporter()
        case _:
            raise EntityNotFoundException(f"Entity {value} not found.")
