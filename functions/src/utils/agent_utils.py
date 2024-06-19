"""Utility functions for the Agents."""

from random import choice

from src import exceptions
from src.models.graph import Graph
from src.models.node import Node
from src.models.path import Path

from functions.src.models.position import Position


def gen_random_path(
    state: Graph, current_pos: Position, move_history: list[Position]
) -> tuple[list[Position], Path]:
    """
    Generate a random path given the context of the current state.

    Parameters
    ----------
    `state` : `Graph`
        The full game board.
    `current_pos` : `Position`
        The agents current position.
    `move_history` : `list[Position]`

    Returns
    -------
    `tuple[list[Position], Path]`
        A tuple containing the list of targets and the path to the first target.
    """
    target = []
    target.append(state.random_node().position)
    # Find path to target
    path = state.shortest_path_to(current_pos, target[0])
    if len(move_history) > 0:
        # If the agent has a move history, check that the agent
        # is not moving backwards
        while path.backwards(move_history):
            target.pop(0)
            target.append(state.random_node().position)
            path = state.shortest_path_to(current_pos, target[0])
    return (target, path)


def choose_random_turn(state: Graph, node: Node) -> Node:
    """
    Chooses a random direction to turn at a junction.

    Parameters
    ----------
    `state` : `Graph`
        The state at the current time.
    `node` : `Node`
        The current position to be used.

    Returns
    -------
    `Node`
        A random node which is adjacent to the current position.
    """
    if not state.is_junction(node):
        raise exceptions.InvalidNodeException("Node is not junction")
    adjacent = state.get_adjacent(node)
    return choice(adjacent)
