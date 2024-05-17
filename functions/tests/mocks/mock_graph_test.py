"""Mocks for the graph."""

from src.models.graph import Graph
from src.services import level_handler
from src.utils import level_utils


def mock_graph() -> Graph:
    """Generate a mock version of a graph."""
    array = level_handler.get_map(1)
    return level_utils.array_to_graph(array)
