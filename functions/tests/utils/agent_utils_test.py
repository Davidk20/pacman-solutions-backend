"""Tests for the Agent utility functions."""

from src.models.graph import Graph
from src.models.node import Node
from src.models.position import Position
from src.utils import agent_utils

# pylint: disable=redefined-outer-name
# fixtures causing error but this is the expected use.

# pylint: disable=R0801
# Duplicate fixtures needed for tests.


def test_random_turn(graph: Graph):
    """Test that a random choice of turn can be obtained."""
    n1 = graph.find_node_by_pos(Position(0, 0))
    actual = agent_utils.choose_random_turn(graph, n1)
    assert isinstance(actual, Node) and actual in graph.get_adjacent(n1)
