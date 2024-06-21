"""
Model storing a collection of `GameState` objects to make up
the full representation of a game.
"""

from src.models.game_state import GameState


class GameStateStore:
    """
    Model storing a collection of `GameState` objects to make up
    the full representation of a game.
    """

    def __init__(self) -> None:
        """
        Initialise the class.
        """
        self.store: list[GameState] = []
        """
        Store containing a list of the states showing the progression
        through the game simulation.
        """

    def add(self, state: GameState) -> None:
        """
        Append a snapshot to `GameStateStore`.

        While the list is assumed already sorted as snapshots should be inserted
        chronologically, it is sorted after appending to ensure this. It is also
        sorted here rather than in the `get` function as if a snapshot is appended
        out of order, it will then need to be re-sorted on every call of `get`
        whereas sorting at time of insertion means any out of position snapshot
        will always be moved to the correct position.

        Parameters
        ----------
        `state` : `GameState`
            The state to be appended.
        """
        self.store.append(state)
        self.store.sort(key=lambda state: state.time, reverse=False)

    def get(self) -> list[GameState]:
        """
        Returns the store of the game snapshots.

        Returns
        -------
        A list of `GameState` snapshots.
        """
        return self.store

    def to_json(self) -> dict:
        """
        Format the `GameStateStore` into a JSON object for communication
        with the front-end.

        Returns
        -------
        `list[dict]`
            A list containing a dictionary for each `GameState`.
        """
        states = []
        for state in self.store:
            states.append(
                {
                    "time": state.time,
                    "state": state.board_state,
                    "energised": state.energised,
                    "score": state.score,
                }
            )
        json = {"states": states}
        return json
