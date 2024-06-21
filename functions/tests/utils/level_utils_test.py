"""Tests on the level utility functions."""

from tests.mocks.mock_graph_test import mock_graph

from functions.src.models.position import Position
from functions.src.services import level_handler
from functions.src.utils import level_utils


def test_graph_to_array_size():
    """
    Test that the array returned by the conversion function
    is the correct size.
    """
    graph = mock_graph()
    array = level_utils.graph_to_array(graph)
    assert len(array) == 31
    assert len(array[0]) == 28


def test_graph_to_array_conversion():
    """Test that the conversion is valid."""
    assert level_utils.graph_to_array(mock_graph()) == level_handler.get_map(1)


def test_array_to_graph():
    """
    Tests that the flood search correctly finds all nodes in the first level.

    - In a 28x31 grid, there are 868 possible positions.
    - There are 559 wall points within this grid.
    - 868 - 559 = 309 playable spaces
    """
    array = level_handler.get_map(1)
    graph = level_utils.array_to_graph(array)
    assert graph.num_of_nodes() == 312


def test_in_bounds():
    """Test that a valid position is identified."""
    assert level_utils.in_bounds(31, 28, Position(1, 1))


def test_out_of_bounds():
    """Test that an out-of-bounds position is identified."""
    assert not level_utils.in_bounds(31, 28, Position(28, 14))


def test_first_non_wall_node():
    """Test that the first playable space can be found."""
    assert level_utils.first_non_wall_node(level_handler.get_map(1)) == Position(1, 1)
