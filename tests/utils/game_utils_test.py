"""Tests for the game utils."""

import pytest
from src import exceptions
from src.models import environment
from src.models import pickups
from src.models.agents import ghost_agent
from src.models.agents.pacman_agent import PacmanAgent
from src.models.node import Node
from src.utils import game_utils
from tests.mocks import mock_agent_test


@pytest.fixture(scope="function")
def agent_teleporter_node():
    """Returns a node containing an agent and a teleporter."""
    e1 = environment.Teleporter()
    e2 = PacmanAgent([], (0, 0))
    node: Node = Node((0, 0), e1)
    node.add_entity(e2)
    yield node


@pytest.fixture(scope="function")
def ghost_pickup_node():
    """Returns a node containing a ghost and a pickup."""
    e1 = pickups.PacDot()
    e2 = mock_agent_test.mock_ghost()
    node: Node = Node((0, 0), e1)
    node.add_entity(e2)
    yield node


@pytest.fixture(scope="function")
def higher_pacman_ghost_node():
    """Returns a node with a ghost and Pac-Man in the higher position."""
    e1 = mock_agent_test.mock_ghost()
    e2 = PacmanAgent([], (0, 0))
    node: Node = Node((0, 0), e1)
    node.add_entity(e2)
    yield node


@pytest.fixture(scope="function")
def lower_pacman_ghost_node():
    """Returns a node with a ghost and Pac-Man in the lower position."""
    e1 = PacmanAgent([], (0, 0))
    e2 = mock_agent_test.mock_ghost()
    node: Node = Node((0, 0), e1)
    node.add_entity(e2)
    yield node


def test_agent_teleporter_collision(agent_teleporter_node: Node):
    """When an agent collides with a teleporter, nothing happens."""
    game_utils.handle_collision(agent_teleporter_node)
    assert agent_teleporter_node.contains(
        environment.Teleporter
    ) and agent_teleporter_node.contains(PacmanAgent)


def test_ghost_pickup_collision(ghost_pickup_node: Node):
    """When a ghost collides with a pickup, nothing happens."""
    game_utils.handle_collision(ghost_pickup_node)
    assert ghost_pickup_node.contains(pickups.PacDot) and ghost_pickup_node.contains(
        ghost_agent.GhostAgent
    )


def test_higher_pacman_ghost_collision(higher_pacman_ghost_node: Node):
    """
    Tests a collision between Pac-Man and a ghost when Pac-Man is in the higher role.

    For this test, it is assumed that Pac-Man is not energised and it is then expected
    that Pac-Man will die.
    """
    with pytest.raises(exceptions.PacManDiedException):
        game_utils.handle_collision(higher_pacman_ghost_node)


def test_lower_pacman_ghost_collision(lower_pacman_ghost_node: Node):
    """
    Tests a collision between Pac-Man and a ghost when Pac-Man is in the lower role.

    For this test, it is assumed that Pac-Man is not energised and it is then expected
    that Pac-Man will die.
    """
    with pytest.raises(exceptions.PacManDiedException):
        game_utils.handle_collision(lower_pacman_ghost_node)
