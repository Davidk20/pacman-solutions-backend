"""Utility functions for the Agents."""
from random import choice

from src import exceptions
from src.models.graph import Graph
from src.models.node import Node
from src.models.path import Path


def gen_random_path(
    state: Graph, current_pos: tuple[int, int], move_history: list[tuple[int, int]]
) -> tuple[list[tuple[int, int]], Path]:
    """
    Generate a random path given the context of the current state.

    Parameters
    ----------
    `state` : `Graph`
        The full game board.
    `current_pos` : `tuple[int, int]`
        The agents current position.
    `move_history` : `list[tuple[int, int]]`

    Returns
    -------
    `tuple[list[tuple[int, int]], Path]`
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


def choose_random_turn(state: Graph, node: Node, prev_pos: tuple[int, int]) -> Node:
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
    if not state.is_junction(node, prev_pos):
        raise exceptions.InvalidNodeException("Node is not junction")
    adjacent = state.get_adjacent(node)
    return choice(adjacent)
