"""Generic fixtures for tests."""

import pytest
from tests.mocks.mock_agent_test import mock_ghost

from functions.src.models import environment, pickups
from functions.src.models.agents.pacman_agent import PacmanAgent
from functions.src.models.graph import Graph
from functions.src.models.node import Node
from functions.src.models.position import Position

# pylint: disable=redefined-outer-name
# fixtures causing error but this is the expected use.


@pytest.fixture(autouse=True)
def graph():
    """Generate an instance of Graph for testing"""
    graph = Graph()
    yield graph


@pytest.fixture(scope="session", autouse=True)
def node():
    """Generate an instance of a Node for testing"""
    node = Node((0, 0), pickups.PacDot())
    yield node


@pytest.fixture(scope="session", autouse=True)
def nodes():
    """Generate an list of a Node for testing"""
    nodes = [
        Node((0, 0), PacmanAgent([Position(0, 0)], Position(0, 0))),
        Node((0, 1), pickups.PacDot()),
        Node((0, 2), pickups.PowerPellet()),
        Node((0, 3), pickups.Empty()),
        Node((0, 4), environment.Teleporter()),
        Node((0, 5), environment.Teleporter()),
        Node((0, 6), mock_ghost()),
        Node((0, 7), pickups.PacDot()),
        Node((0, 8), pickups.PacDot()),
        Node((0, 9), pickups.PacDot()),
    ]
    yield nodes


@pytest.fixture(scope="session", autouse=True)
def adjacency_list():
    """Generate the adjacency list for testing, uses `nodes`."""
    adjacency_list: dict[Position, list[Position]] = {
        Position(0, 0): [Position(0, 1), Position(0, 2), Position(0, 6)],
        Position(0, 1): [Position(0, 3), Position(0, 5)],
        Position(0, 2): [Position(0, 1), Position(0, 4)],
        Position(0, 3): [Position(0, 1), Position(0, 0)],
        Position(0, 4): [Position(0, 1), Position(0, 5)],
        Position(0, 5): [Position(0, 3), Position(0, 2)],
        Position(0, 6): [Position(0, 1), Position(0, 4), Position(0, 7)],
        Position(0, 7): [Position(0, 8)],
        Position(0, 8): [Position(0, 9)],
        Position(0, 9): [Position(0, 6)],
    }
    yield adjacency_list


@pytest.fixture(scope="function", autouse=True)
def compiled_graph():
    """
    Returns a fully-mapped graph.

    For use where testing this functionality is not required.
    """
    graph = Graph()
    nodes = [
        Node((0, 0), PacmanAgent([Position(0, 0)], Position(0, 0))),
        Node((0, 1), pickups.PacDot()),
        Node((0, 2), pickups.PowerPellet()),
        Node((0, 3), pickups.Empty()),
        Node((0, 4), environment.Teleporter()),
        Node((0, 5), environment.Teleporter()),
        Node((0, 6), mock_ghost()),
        Node((0, 7), pickups.PacDot()),
        Node((0, 8), pickups.PacDot()),
        Node((0, 9), pickups.PacDot()),
    ]
    adjacency_list: dict[Position, list[Position]] = {
        Position(0, 0): [Position(0, 1), Position(0, 2), Position(0, 6)],
        Position(0, 1): [Position(0, 3), Position(0, 5)],
        Position(0, 2): [Position(0, 1), Position(0, 4)],
        Position(0, 3): [Position(0, 1), Position(0, 0)],
        Position(0, 4): [Position(0, 1), Position(0, 5)],
        Position(0, 5): [Position(0, 3), Position(0, 2)],
        Position(0, 6): [Position(0, 1), Position(0, 4), Position(0, 7)],
        Position(0, 7): [Position(0, 8)],
        Position(0, 8): [Position(0, 9)],
        Position(0, 9): [Position(0, 6)],
    }

    for node in nodes:
        graph.add_node(node)

    graph.map_edges(adjacency_list)
    yield graph
