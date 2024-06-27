"""Service managing writing output to files."""

import csv
import json
import time


def write_to_csv(data) -> None:
    """Writes the given text to a CSV file."""
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    unique_filename = f"pacman_{timestamp}.csv"
    print(f"beginning write to {unique_filename}")
    with open(unique_filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            "agent_name",
            "run_id",
            "time_seconds",
            "time_ticks",
            "final_score",
            "state_time",
            "energised",
            "state_score",
            "board_state",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for agent in data:
            for run in agent.snapshots:
                for state in run.states:
                    writer.writerow(
                        {
                            "agent_name": agent.name,
                            "run_id": run.run_id,
                            "time_seconds": run.time_seconds,
                            "time_ticks": run.time_ticks,
                            "final_score": run.final_score,
                            "state_time": state.time,
                            "board_state": json.dumps(
                                state.board_state
                            ),  # Convert board_state to a JSON string for CSV
                            "energised": state.energised,
                            "state_score": state.score,
                        }
                    )
