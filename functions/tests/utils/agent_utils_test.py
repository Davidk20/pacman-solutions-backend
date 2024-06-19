import pytest
from src.models.agents.pacman_agent import PacmanAgent
from src.models.graph import Graph
from src.models.node import Node
from src.models.position import Position
from src.utils import agent_utils
from tests.mocks.mock_agent_test import mock_ghost

from functions.src.models import environment, pickups


@pytest.fixture(scope="function", autouse=True)
def graph():
    """
    Returns a fully-mapped graph.

    For use where testing this functionality is not required.
    """
    graph = Graph()
    nodes = [
        Node((0, 0), PacmanAgent([(0, 0)], (0, 0))),
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


def test_random_turn(graph: Graph):
    """Test that a random choice of turn can be obtained."""
    n1 = graph.find_node_by_pos(Position(0, 0))
    actual = agent_utils.choose_random_turn(graph, n1)
    assert isinstance(actual, Node) and actual in graph.get_adjacent(n1)
