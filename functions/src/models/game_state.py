"""Model storing the state of the game at an instance in time."""

from dataclasses import dataclass


@dataclass
class GameState:
    """Model storing the state of the game at an instance in time."""

    time: int
    board_state: list[list[int]]
    energised: bool
    score: int
