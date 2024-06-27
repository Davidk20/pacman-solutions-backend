"""Analytics tool designed to compare the performance of various agents."""

import threading
import time
from dataclasses import dataclass
from typing import Type

from src.models.agents.custom_agents.adventurous import AdventurousPacMan
from src.models.agents.custom_agents.greedy import GreedyPacMan
from src.models.agents.custom_agents.inactive import InactivePacMan
from src.models.agents.custom_agents.informed import InformedPacMan
from src.models.agents.custom_agents.unplanned import UnplannedPacMan
from src.models.agents.pacman_agent import PacmanAgent
from src.models.game_state import GameState
from src.services import game_manager
from src.services.file_writer import write_to_csv


@dataclass
class RunSnapshot:
    """Model representing the full analytics data for a single run."""

    name: str
    """The name of the agent."""
    run_id: str
    """The unique ID for the run"""
    time_seconds: float
    """The time taken to complete a run in seconds."""
    time_ticks: int
    """The time taken to complete a run in internal ticks."""
    final_score: int
    """The final score of the run."""
    states: list[GameState]
    """The individual states of this run."""


@dataclass
class AgentSnapshot:
    """Model representing the analytics snapshot of a single agent."""

    name: str
    """The name of the agent."""
    snapshots: list[RunSnapshot]
    """The collection of snapshots."""

    @property
    def avg_time(self) -> float:
        """The average time an agent takes to complete."""
        return sum((run.time_ticks for run in self.snapshots)) / len(self.snapshots)

    @property
    def avg_real_time(self) -> float:
        """The average time an agent takes to complete (in seconds)."""
        return round(
            sum((run.time_seconds for run in self.snapshots)) / len(self.snapshots), 3
        )

    @property
    def avg_score(self) -> float:
        """The average score an agent achieves."""
        return sum((run.final_score for run in self.snapshots)) / len(self.snapshots)


class PacmanAnalytics:
    """Analytics tool designed to compare the performance of various agents."""

    def __init__(
        self, output: bool, runs: int = 10, custom_agents: list[Type[PacmanAgent]] = []
    ):  # pylint: disable=W0102
        """
        Initialise the class.

        Parameters
        ----------
        `runs` : `int` DEFAULT = `10`
            The number of iterations each agent will be tested for.
        `custom_agents` : `list[PacmanAgent]` DEFAULT = `[]`
            Any custom agents the user wishes to compare against
        """
        self.runs = runs
        self.agents: list[Type[PacmanAgent]] = [
            InactivePacMan,
            UnplannedPacMan,
            InformedPacMan,
            GreedyPacMan,
            AdventurousPacMan,
        ] + custom_agents
        self.results: list[AgentSnapshot] = []
        self.run_models()
        self.render_data()
        if output:
            write_to_csv(self.results)

    def run_model(self, agent: Type[PacmanAgent]):
        """Set up and run a single model."""
        ag_snapshot: AgentSnapshot = AgentSnapshot(agent.__name__, [])
        for i in range(self.runs):
            snapshot: RunSnapshot = RunSnapshot(
                agent.__name__, f"{agent.__name__}_{i}", 0, 0, 0, []
            )
            print(f"Running {agent.__name__} iteration {i+1}")
            start_time = time.time()
            game = game_manager.GameManager(
                1, game_manager.RunConfiguration.ANALYTIC, custom_pacman=agent
            )
            try:
                results = game.game_loop()
                snapshot.time_seconds = time.time() - start_time
                snapshot.states = [
                    GameState(
                        time=data["time"],
                        board_state=data["state"],
                        energised=data["energised"],
                        score=data["score"],
                    )
                    for data in results["states"]
                ]
                snapshot.final_score = results["score"]
                snapshot.time_ticks = results["time"]
                ag_snapshot.snapshots.append(snapshot)
                print(f"{agent.__name__} run {i+1} complete.")
            except IndexError:
                print(f"{agent.__name__} run {i+1} failed.")
        self.results.append(ag_snapshot)

    def run_models(self):
        """Run the models and collect the data."""
        runs: list[threading.Thread] = []
        for agent in self.agents:
            runs.append(
                threading.Thread(
                    target=self.run_model, args=(agent,), name=agent.__name__
                )
            )
        for run in runs:
            run.start()
        for run in runs:
            run.join()

    def render_data(self):
        """Use the data to render a comparison of models."""
        print("############################")
        print("RUN COMPLETE")
        print("############################")
        for agent in self.results:
            print(f"{agent.name} - {len(agent.snapshots)} runs")
            print(f"avg time (in seconds) = {agent.avg_real_time}")
            print(f"avg time (in game) = {agent.avg_time}")
            print(f"avg score = {agent.avg_score}")
            print("\n")
