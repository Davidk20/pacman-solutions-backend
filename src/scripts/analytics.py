"""Analytics tool designed to compare the performance of various agents."""

import time
from typing import Type

from src.models.agents.custom_agents.inactive import InactivePacMan
from src.models.agents.custom_agents.informed import (
    InformedPacMan,
)
from src.models.agents.custom_agents.random import RandomPacMan
from src.models.agents.pacman_agent import PacmanAgent
from src.services import game_manager


class PacmanAnalytics:
    """Analytics tool designed to compare the performance of various agents."""

    def __init__(self, runs: int = 10, custom_agents: list[Type[PacmanAgent]] = []):
        """
        Initialise the class.

        - It is assumed that the analytics will be run on the first level as this
        is the most proven level and the easiest for testing.

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
            RandomPacMan,
            InformedPacMan,
        ] + custom_agents
        self.results = {}
        self.run_models()
        self.render_data()

    def run_models(self):
        """Run the models and collect the data."""
        for agent in self.agents:
            runs: list[dict] = []
            for _ in range(self.runs):
                start_time = time.time()
                game = game_manager.GameManager(
                    1, game_manager.RunConfiguration.ANALYTIC, custom_pacman=agent
                )
                results = game.game_loop()
                results["time_real"] = time.time() - start_time
                runs.append(results)
            self.results[agent.__name__] = runs

    def render_data(self):
        """Use the data to render a comparison of models."""
        print("############################")
        print("RUN COMPLETE")
        print("############################")
        print(f"\nAfter {self.runs} runs:\n")
        for agent, data in self.results.items():
            print(agent)
            avg_time_real = round(
                (sum([run["time_real"] for run in data]) / self.runs), 4
            )
            avg_time_game = sum([run["time_game"] for run in data]) / self.runs
            avg_score = sum([run["score"] for run in data]) / self.runs
            print(f"avg time (in seconds) = {avg_time_real}")
            print(f"avg time (in game) = {avg_time_game}")
            print(f"avg score = {avg_score}")
            print("\n")
