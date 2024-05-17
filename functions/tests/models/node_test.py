"""Tests for the Node model."""

import pytest
from src import exceptions
from src.models.agents.placeholder_agent import PlaceholderAgent
from src.models.node import Node
from src.models.pickups import Empty, PacDot


@pytest.fixture(scope="function", autouse=True)
def empty_node():
    yield Node((0, 0), Empty())


@pytest.fixture(scope="function", autouse=True)
def pickup_node():
    yield Node((0, 0), PacDot())


def test_valid_node_initialisation():
    """Valid nodes should be correctly instantiated."""
    test_node = Node((0, 0), PacDot())
    assert isinstance(test_node, Node)


def test_empty_node(empty_node: Node):
    """Test that empty nodes are identified."""
    assert empty_node.empty()


def test_no_collision(empty_node: Node):
    """Tests that standard nodes do not collide."""
    assert not empty_node.is_collision()


def test_collision(pickup_node: Node):
    """Tests that collisions are identified."""
    pickup_node.add_entity(PlaceholderAgent("", 0))


def test_add_to_empty(empty_node: Node):
    """Tests adding entity to empty node."""
    empty_node.add_entity(PacDot())
    assert empty_node.contains(PacDot)


def test_add_dupe_pickup(pickup_node: Node):
    """Test adding dupe pickup to node raises error."""
    with pytest.raises(exceptions.InvalidNodeException):
        pickup_node.add_entity(PacDot())


def test_remove_entity(pickup_node: Node):
    """Test removal of entity from Node."""
    pickup_node.remove_entity(pickup_node.get_higher_entity())
    assert pickup_node.empty()


def test_remove_empty_node(empty_node: Node):
    """Test removal of empty node raises error."""
    with pytest.raises(exceptions.InvalidNodeException):
        empty_node.remove_entity(PacDot())


def test_get_higher_entity(pickup_node: Node):
    """Test that the higher priority entity is returned"""
    pickup_node.add_entity(PlaceholderAgent("", 0))
    assert isinstance(pickup_node.get_higher_entity(), PlaceholderAgent)


def test_get_higher_agent(empty_node: Node):
    """Test that the higher agent is returned when the node contains two agents."""
    empty_node.add_entity(PlaceholderAgent("", 0))
    empty_node.add_entity(PlaceholderAgent("", 1))
    assert empty_node.get_higher_entity().value() == 1


def test_get_lower_entity(pickup_node: Node):
    """Test that the higher priority entity is returned"""
    pickup_node.add_entity(PlaceholderAgent("", 0))
    assert isinstance(pickup_node.get_lower_entity(), PacDot)


def test_get_lower_agent(empty_node: Node):
    """Test that the lower agent is returned when the node contains two agents."""
    empty_node.add_entity(PlaceholderAgent("", 0))
    empty_node.add_entity(PlaceholderAgent("", 1))
    assert empty_node.get_lower_entity().value() == 0


def test_get_empty_entity(empty_node: Node):
    """Test that empty entity is returned from empty node."""
    assert isinstance(empty_node.get_higher_entity(), Empty)
    assert isinstance(empty_node.get_lower_entity(), Empty)


def test_get_specific_pickup(empty_node: Node):
    empty_node.add_entity(PacDot())
    assert isinstance(empty_node.get_entity(PacDot), PacDot)


def test_get_specific_agent(empty_node: Node):
    empty_node.add_entity(PacDot())
    empty_node.add_entity(PlaceholderAgent("", 0))
    assert isinstance(empty_node.get_entity(PlaceholderAgent), PlaceholderAgent)


def test_get_specific_not_found(empty_node: Node):
    with pytest.raises(exceptions.InvalidNodeException):
        empty_node.get_entity(PacDot)
