"""Generic functions to be applied to instances of Levels."""

from src import constants
from src.exceptions import NodeNotFoundException
from src.models.graph import Graph
from src.models.node import Node
from src.utils.entity_utils import convert_value_to_entity
from src.utils.entity_utils import EntityNotFoundException


def print_level(level: list[list[int]]) -> None:
    """Prints a formatted version of the 2-D array level."""
    for row in level:
        row_str = str(row)
        row_str = row_str.replace(" 0,", "  0,")
        row_str = row_str.replace(" 1,", "  1,")
        row_str = row_str.replace(" 2,", "  2,")
        print(row_str)


def array_to_graph(level: list[list[int]]) -> Graph:
    """
    Convert the map from an array into Graph.

    Searches the level using "Flood Fill" search to filter out walls
    and leave only the paths which are then used to generate the graph.

    Inspired by https://lvngd.com/blog/flood-fill-algorithm-python/

    Parameters
    ----------
    `level` : `list[list[int]]`
        The level to convert

    Returns
    -------
    A populated `Graph` object.
    """
    height = len(level)
    width = len(level[0])
    # queue to store the positions to be looked into
    queue: list[tuple[int, int]] = [first_non_wall_node(level)]
    adjacency_list: dict[tuple[int, int], list[tuple[int, int]]] = {}
    graph = Graph()

    while len(queue) > 0:
        current = queue.pop(0)

        # invalid positions should be ignored
        if (
            not in_bounds(height, width, current)
            or is_wall(level, current)
            or current in adjacency_list.keys()
        ):
            continue

        # if is valid space then build node and add adjacents
        entity = convert_value_to_entity(level[current[1]][current[0]])
        graph.add_node(Node(current, entity))
        adjacency_list[current] = []
        expansions = [
            (current[0] + 1, current[1]),
            (current[0], current[1] + 1),
            (current[0], current[1] - 1),
            (current[0] - 1, current[1]),
        ]
        for expansion in expansions:
            if in_bounds(height, width, expansion):
                if not is_wall(level, expansion):
                    adjacency_list[current].append(expansion)
                    queue.append(expansion)
    graph.map_edges(adjacency_list)
    return graph


def graph_to_array(graph: Graph) -> list[list[int]]:
    """
    Convert a `Graph` representation of a level into a 2-D array.

    Parameters
    ----------
    `graph` : `Graph`
        The graph to be converted.

    Returns
    -------
    A 2-D list containing the level.
    """
    level = []
    for row in range(constants.PACMAN_BOARD_HEIGHT):
        level.append([])
        for column in range(constants.PACMAN_BOARD_WIDTH):
            try:
                node = graph.find_node_by_pos((column, row))
                if node.empty():
                    level[row].append(0)
                else:
                    level[row].append(node.get_higher_entity().value())
            except NodeNotFoundException:
                level[row].append(99)
                continue
    return level


def in_bounds(height: int, width: int, pos: tuple[int, int]) -> bool:
    """
    Check a position is within the bounds of the map.

    Parameters
    ----------
    `height` : `int`
        The height of the map.
    `width` : `int`
        The width of the map.
    `pos` : `tuple[int, int]`
        The position to check

    Returns
    -------
    `True` if the position is within bounds.
    """
    return pos[0] >= 0 and pos[0] < width and pos[1] >= 0 and pos[1] < height


def is_wall(map: list[list[int]], pos: tuple[int, int]) -> bool:
    """
    Checks if the specified space is a `Wall`.

    Parameters
    ----------
    `map` : `list[list[int]]`
        The level to use as reference.
    `pos` : `tuple[int, int]`
        The position to check.

    Returns
    -------
    `True` if the space is filled with a wall.
    """
    return map[pos[1]][pos[0]] == 99


def first_non_wall_node(map: list[list[int]]) -> tuple[int, int]:
    """
    Find and return the first position within the map.

    This should be the upper-leftmost node which is not a wall.

    Parameters
    ----------
    `map` : `list[list[int]]`
        The level to search.

    Returns
    -------
    The position of the first non-wall node.
    """
    for y in range(len(map)):
        for x in range(len(map[0])):
            if map[y][x] != 99:
                return (x, y)
    raise EntityNotFoundException("No non-wall nodes found.")
