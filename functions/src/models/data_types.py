"""File containing a set of models linking JSON objects to data types."""

from typing import TypedDict

from src.models.position import Position


class LevelData(TypedDict):
    """Typed representation of a level as stored in levels.json"""

    name: str
    map: list[list[int]]
    homes: dict[str, list[list[int]]]
    respawn: dict[str, list[list[int]]]


class AgentHomes(TypedDict):
    """Typed representation of the agents home paths data structure."""

    pacman: list[Position]
    blinky: list[Position]
    pinky: list[Position]
    inky: list[Position]
    clyde: list[Position]


class AgentRespawn(TypedDict):
    """Typed representation of the agents respawn points."""

    pacman: Position
    blinky: Position
    pinky: Position
    inky: Position
    clyde: Position
