"""Enum containing the types of movement possible for agents."""

from enum import Enum


class MovementTypes(Enum):
    """Enum containing the types of movement possible for agents."""

    SCATTER = 0
    """
    Movement style only applying to ghosts. Each ghost has a fixed target
    tile, each of which is located just outside a different corner of the maze.
    This movement style will require a ghost agent to also be provided with
    coordinates which they will then target
    """
    CHASE = 1
    """
    Movement style only applying to ghosts. Pac-man's position is used as
    the bearing for the ghosts movement. The degree to which this is used
    will vary between the ghosts to give a degree of variation between
    ghosts.
    """
    FRIGHTENED = 2
    """
    Movement style only applying to ghosts. Each ghost will pseudorandomly
    decide which direction to turn at each junction.
    """
    CUSTOM = 3
    """
    Movement style only applying to Pac-man. Movement is controlled by user
    input. In the interpretation of this project, this instead means
    that movement will be controlled by an agent with planning.
    """
    HOMEBOUND = 4
    """
    Movement style only applying to ghosts. If a Ghost is consumed by Pac-man
    while he is energised, they should return to the "home". This movement type
    will instruct a Ghost to aim for these coordinates.
    """
