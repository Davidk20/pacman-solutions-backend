"""
Service to read and manage the levels.

This service runs as standalone functions as opposed to a class as
`LevelHandler` is used in a number of different classes during a single
run and therefore would mean that the file is open in a number of places
at any one time. Standalone functions mean that the file can be opened
and closed within the lifetime of a function and also prevents the instantiation
of a number of unnecessary files.
"""

import json
import os

from src import exceptions
from src.models import data_types
from src.models.position import Position


def get_levels():
    """
    Parses the levels.json file and returns a dictionary containing the levels
    and their data.

    Returns
    -------
    A `dict` object containing the levels and their data.
    """
    absolute_path = os.path.dirname(__file__)
    relative_path = "../models/levels.json"
    raw_levels = open(os.path.join(absolute_path, relative_path), encoding="utf-8")
    json_data = json.load(raw_levels)
    yield json_data
    raw_levels.close()


def get_level(level_num: int) -> data_types.LevelData:
    """
    Returns all info for a level when provided with the level number.

    Parameters
    ----------
    `level_num` : `int`
        The number of the desired level

    Returns
    -------
    The level data for the desired level
    """
    for levels in get_levels():
        for key, value in levels.items():
            if key == f"level {level_num}":
                return value
    raise exceptions.LevelNotFoundException(level_num)


def get_map(level_num: int) -> list[list[int]]:
    """
    Returns only the map for a given level.

    Parameters level_num: The number of the desired level
    :returns: The map data for the desired level
    """
    level = get_level(level_num)
    if level is not None:
        return level.get("map")  # type: ignore
    raise exceptions.LevelNotFoundException(level_num)


def get_overview() -> list[str]:
    """
    Returns an overview of all levels.

    Returns
    -------
    A list of all of the available levels to be solved.
    """
    available = []
    level: dict
    for levels in get_levels():
        for level in levels.values():
            available.append(level.get("name"))
    return available


def get_homes(level_num: int) -> data_types.AgentHomes:
    """
    Return the homes for all agents.

    Parameters
    ----------
    `level_num` : `int`
        The number of the desired level

    Returns
    -------
    A `dict` containing the mapping of agents to their path of coordinates
    which the agent should follow when returning "home".
    """
    level: data_types.LevelData = get_level(level_num)
    homes: dict[str, list[list[int]]] = level.get("homes")
    formatted_homes: dict[str, list[Position]] = {}
    if homes is None:
        raise exceptions.InvalidLevelConfigurationException(level_num)

    for agent, home in homes.items():
        path: list[Position] = []
        for coord in home:
            # Ignored type as it is a determined number of args for tuple.
            path.append(tuple([coord[0], coord[1]]))  # type: ignore
        formatted_homes[agent] = path
    return formatted_homes  # type: ignore


def get_home(level_num: int, agent: str) -> list[Position]:
    """
    Returns the home path for a given agent.

    Parameters
    ----------
    `level_num` : `int`
        The number of the desired level
    `agent` : `str`
        The name of the agent.

    Returns
    -------
    A `list` containing the path of coordinates which the agent should
    follow when returning "home".
    """
    homes = get_homes(level_num)
    home: list[Position] = []
    agent_home = homes[agent.lower()]
    if agent_home is not None:
        for coord in agent_home:
            # Ignored type as it is a determined number of args for tuple.
            home.append(tuple([coord[0], coord[1]]))  # type: ignore
    else:
        raise exceptions.InvalidLevelConfigurationException(level_num)

    return home


def get_respawn_points(level_num: int) -> data_types.AgentRespawn:
    """
    Return the respawn points for all agents.

    Parameters
    ----------
    `level_num` : `int`
        The number of the desired level

    Returns
    -------
    A `dict` containing the mapping of agents to their respawn points.
    """
    level: data_types.LevelData = get_level(level_num)
    points: dict[str, list[list[int]]] = level.get("respawn")
    formatted_points: dict[str, Position] = {}

    if points is None:
        raise exceptions.InvalidLevelConfigurationException(level_num)

    for agent, point in points.items():
        formatted_points[agent] = Position(point[0], point[1])  # type: ignore
    return formatted_points  # type: ignore
