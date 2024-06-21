"""Utility functions to assist running the game."""

from src.models import environment, pickups
from src.models.agents import ghost_agent
from src.models.agents.pacman_agent import PacmanAgent
from src.models.node import Node


def handle_collision(node: Node) -> None:
    """Handle the collision within a single node between two or more entities."""

    if node.contains(environment.Teleporter):
        # If passing through teleporter, ignore
        return

    # if ghost collides with anything but Pac-Man, ignore
    if node.contains(ghost_agent.GhostAgent) and not node.contains(PacmanAgent):
        return

    # if Pac-Man collides with Ghost
    if node.contains(PacmanAgent) and node.contains(ghost_agent.GhostAgent):
        pacman = node.get_entity(PacmanAgent)
        pacman.handle_consume(node.get_entity(ghost_agent.GhostAgent))

    # if Pac-Man collides with pickup
    if node.contains(PacmanAgent) and node.contains(pickups.Pickup):
        pacman = node.get_entity(PacmanAgent)
        pickup = node.get_entity(pickups.Pickup)
        pacman.handle_consume(pickup)
        node.entities.remove(pickup)
