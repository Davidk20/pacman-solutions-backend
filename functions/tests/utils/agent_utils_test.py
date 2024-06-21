"""Tests for the Agent utility functions."""

from functions.src.models.graph import Graph
from functions.src.models.node import Node
from functions.src.models.position import Position
from functions.src.utils import agent_utils

# pylint: disable=redefined-outer-name
# fixtures causing error but this is the expected use.


def test_random_turn(compiled_graph: Graph):
    """Test that a random choice of turn can be obtained."""
    n1 = compiled_graph.find_node_by_pos(Position(0, 0))
    actual = agent_utils.choose_random_turn(compiled_graph, n1)
    assert isinstance(actual, Node) and actual in compiled_graph.get_adjacent(n1)
