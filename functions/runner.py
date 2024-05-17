"""
Main driver file for running the backend locally.

Inspiration taken from:

https://realpython.com/command-line-interfaces-python-argparse/
"""

import argparse
import sys

from src.scripts.analytics import PacmanAnalytics
from src.services.game_manager import GameManager, RunConfiguration

try:
    print("")
except ModuleNotFoundError:
    print(
        "ERROR - Activate virtual environment before attempting to run driver script."
    )
    sys.exit(1)


class ArgParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write(f"\nError: {message}\n\n")
        self.print_help()
        sys.exit(2)


def main():
    parser = ArgParser(
        prog="main.py",
        description="""
        Pac-Man Solutions - Back-End: AI solutions to abstractions of Pac-Man levels.
        """,
    )

    parser.add_argument(
        "run_config",
        choices=["single", "analytics"],
        help="""
        single = Run single game,
        analytics = Run analytics tool""",
    )

    parser.add_argument(
        "-l", "--level", type=int, help="specify level number as an integer"
    )

    local_options = parser.add_argument_group("Single Run Options")

    local_options.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=0,
        help="enable verbose output - full final state printing",
    )

    local_options.add_argument(
        "-d",
        "--debug",
        action="store_true",
        default=0,
        help="enable debug output - full final state printing + all noteworthy events",
    )

    analytics_options = parser.add_argument_group("Analytics Options")

    analytics_options.add_argument(
        "-o",
        "--output_file",
        action="store",
        type=str,
        help="write the output data to a file",
    )

    analytics_options.add_argument(
        "-r",
        "--runs",
        default=10,
        type=int,
        help="the number of runs completed to assess performance",
    )

    args = parser.parse_args()

    match args.run_config:
        case "local":
            game = GameManager(
                args.level, configuration=RunConfiguration.LOCAL, verbose=args.verbose
            )
            game.game_loop()
        case "analytics":
            PacmanAnalytics(runs=args.runs)


if __name__ == "__main__":
    main()
