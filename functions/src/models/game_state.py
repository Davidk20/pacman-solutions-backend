"""Model storing the state of the game at an instance in time."""

from dataclasses import dataclass


@dataclass
class GameState:
    """Model storing the state of the game at an instance in time."""

    time: int
    """The time corresponding to the snapshot."""
    board_state: list[list[int]]
    """The state of the board in the snapshot."""
    energised: bool
    """Whether Pac-Man is energised in the snapshot."""
    score: int
    """The score in the snapshot."""
