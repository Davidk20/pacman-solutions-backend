"""Tests for the Graph class."""

import pytest
from src import exceptions
from src.models import pickups
from src.models.agents.pacman_agent import PacmanAgent
from src.models.graph import Graph
from src.models.node import Node
from src.models.path import Path
from src.models.position import Position

# pylint: disable=redefined-outer-name
# fixtures causing error but this is the expected use.


def test_add_node(graph: Graph, node: Node):
    """Test that a node is correctly added to the graph."""
    graph.add_node(node)
    assert graph.num_of_nodes() == 1
    assert graph.node_count == 2


def test_add_repeated_node(graph: Graph, node: Node):
    """Test that exception is raised when duplicate node is added."""
    graph.add_node(node)
    with pytest.raises(exceptions.DuplicateNodeException):
        graph.add_node(node)


def test_find_node_by_pos(graph: Graph, node: Node):
    """Test that a node can be found if it is in the graph."""
    graph.add_node(node)
    assert graph.find_node_by_pos(Position(0, 0)) == node


def test_find_node_by_pos_raises(graph: Graph, node: Node):
    """Test that an error is raised if a node cannot be found when not in the graph."""
    graph.add_node(node)
    with pytest.raises(exceptions.NodeNotFoundException):
        graph.find_node_by_pos(Position(0, 1))


def test_find_by_entity(compiled_graph: Graph):
    """Test that a node can be found by searching for entity."""
    result = compiled_graph.find_node_by_entity(pickups.PacDot)
    assert len(result) == 4


def test_map_edges(
    graph: Graph,
    nodes: list[Node],
    adjacency_list: dict[Position, list[Position]],
):
    """Test that edges are correctly mapped using the adjacency matrix."""
    for node in nodes:
        graph.add_node(node)

    graph.map_edges(adjacency_list)

    assert graph.num_of_edges() == 21


def test_bfs(
    graph: Graph,
    nodes: list[Node],
    adjacency_list: dict[Position, list[Position]],
):
    """Test that bfs correctly traverses the graph."""
    for node in nodes:
        graph.add_node(node)

    graph.map_edges(adjacency_list)
    assert len(graph.bfs(Position(0, 0))) == 10


def test_is_connected(compiled_graph: Graph):
    """Test that a connected graph is correctly evaluated."""
    assert compiled_graph.is_connected()


def test_agent_collision_with_pickup(compiled_graph: Graph):
    """Tests that an agent correctly handles collision with an item."""
    with pytest.raises(exceptions.CollisionException):
        compiled_graph.move_agent(Position(0, 0), Position(0, 1), PacmanAgent)


def test_agent_collision_with_ghost(compiled_graph: Graph):
    """Tests that an agent correctly handles collision with a ghost."""
    with pytest.raises(exceptions.CollisionException):
        compiled_graph.move_agent(Position(0, 0), Position(0, 6), PacmanAgent)


def test_agent_move_no_collision(compiled_graph: Graph):
    """Tests that an agent can move into an empty space."""
    compiled_graph.move_agent(Position(0, 0), Position(0, 3), PacmanAgent)


def test_move_nowhere(compiled_graph: Graph):
    """Test that Pac-Man is able to "move" to the same spot."""
    compiled_graph.move_agent(Position(0, 0), Position(0, 0), PacmanAgent)
    assert compiled_graph.find_node_by_entity(PacmanAgent)[0].position == Position(0, 0)


def test_non_repeating_cycle(compiled_graph: Graph, nodes: list[Node]):
    """Test that non-repeating paths are detected."""
    test_1 = [nodes[0], nodes[1], nodes[2], nodes[3], nodes[4]]
    test_2 = [nodes[4], nodes[3], nodes[2], nodes[1], nodes[0]]
    test_3 = [nodes[2], nodes[0], nodes[5], nodes[3], nodes[2]]
    test_4 = [nodes[5], nodes[5], nodes[1], nodes[4], nodes[2]]
    test_5 = [nodes[6], nodes[5], nodes[5], nodes[6], nodes[2]]
    assert not compiled_graph.is_repeated_cycle(test_1)
    assert not compiled_graph.is_repeated_cycle(test_2)
    assert not compiled_graph.is_repeated_cycle(test_3)
    assert not compiled_graph.is_repeated_cycle(test_4)
    assert not compiled_graph.is_repeated_cycle(test_5)


def test_repeating_cycle(compiled_graph: Graph, nodes: list[Node]):
    """Test that repeating paths are detected."""
    test_1 = [nodes[0], nodes[1], nodes[2], nodes[3], nodes[4], nodes[1], nodes[2]]
    test_2 = [nodes[6], nodes[5], nodes[6], nodes[5], nodes[4], nodes[1], nodes[2]]
    test_3 = [nodes[4], nodes[1], nodes[2], nodes[3], nodes[4], nodes[1], nodes[2]]
    test_4 = [nodes[0], nodes[0], nodes[0], nodes[0], nodes[0], nodes[0], nodes[0]]
    assert compiled_graph.is_repeated_cycle(test_1)
    assert compiled_graph.is_repeated_cycle(test_2)
    assert compiled_graph.is_repeated_cycle(test_3)
    assert compiled_graph.is_repeated_cycle(test_4)


def test_find_all_paths_node_not_found(compiled_graph: Graph):
    """
    Test that an exception is raised when an invalid node is passed as an argument.
    """
    with pytest.raises(exceptions.NodeNotFoundException):
        compiled_graph.find_paths_between(Position(100, 0), Position(0, 0))


def test_find_all_paths_already_at_goal(compiled_graph: Graph, nodes: list[Node]):
    """Test that a single path is returned when the starting node is the goal node."""
    assert compiled_graph.find_paths_between(Position(0, 0), Position(0, 0)) == [
        Path([nodes[0]])
    ]


def test_find_all_paths_simple_path(compiled_graph: Graph, nodes: list[Node]):
    """Test that a simple, single path can be found connecting two nodes."""
    path = Path([nodes[6], nodes[7], nodes[8], nodes[9]])
    assert compiled_graph.find_paths_between(Position(0, 6), Position(0, 9)) == [path]


def test_find_all_paths_multiple_paths(compiled_graph: Graph, nodes: list[Node]):
    """Test that multiple paths are returned where appropriate."""
    path_1 = Path(
        [nodes[1], nodes[3], nodes[0], nodes[6], nodes[7], nodes[8], nodes[9]]
    )
    path_2 = Path(
        [nodes[1], nodes[5], nodes[3], nodes[0], nodes[6], nodes[7], nodes[8], nodes[9]]
    )
    assert compiled_graph.find_paths_between(Position(0, 1), Position(0, 9)) == [
        path_1,
        path_2,
    ]


def test_find_shortest_path(compiled_graph: Graph, nodes: list[Node]):
    """Test that the shortest path is found."""
    path = Path([nodes[1], nodes[3], nodes[0], nodes[6], nodes[7], nodes[8], nodes[9]])
    assert compiled_graph.shortest_path_to(Position(0, 1), Position(0, 9)) == path


def test_remaining_pickups(compiled_graph: Graph):
    """
    Test that the number of pickups remaining is correctly counted.
    """
    assert compiled_graph.remaining_pickups() == 5


def test_is_junction(compiled_graph: Graph):
    "Test that the node is a junction."
    n1 = compiled_graph.find_node_by_pos(Position(0, 0))
    n3 = compiled_graph.find_node_by_pos(Position(0, 6))
    assert compiled_graph.is_junction(n1)
    assert compiled_graph.is_junction(n3)


def test_not_junction(compiled_graph: Graph):
    """Test that nodes are not a junction."""
    n1 = compiled_graph.find_node_by_pos(Position(0, 7))
    n2 = compiled_graph.find_node_by_pos(Position(0, 8))
    n3 = compiled_graph.find_node_by_pos(Position(0, 9))
    assert not compiled_graph.is_junction(n1)
    assert not compiled_graph.is_junction(n2)
    assert not compiled_graph.is_junction(n3)


def test_adjacency(compiled_graph: Graph):
    """Checks that a nodes adjacent nodes are returned."""
    n1 = compiled_graph.find_node_by_pos(Position(0, 7))
    n2 = compiled_graph.find_node_by_pos(Position(0, 8))
    assert compiled_graph.get_adjacent(n1) == [n2]


def test_path_to_jct(compiled_graph: Graph):
    """
    Check that the path can be found to the next junction.

    As this function uses BFS, the shortest path will
    always be returned first, this will test that the
    shortest path ends at the closest junction.
    """
    paths = compiled_graph.find_path_to_next_jct(Position(0, 7))
    for path in paths:
        if path.route[-1].position == (0, 6):
            assert path.route[-1].position == (0, 6)
