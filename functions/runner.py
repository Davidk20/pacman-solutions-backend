"""
Main driver file for running the backend locally.

Inspiration taken from:

https://realpython.com/command-line-interfaces-python-argparse/
"""

import argparse
import sys

from main import app

from functions.src.scripts.analytics import PacmanAnalytics
from functions.src.services.game_manager import GameManager, RunConfiguration

try:
    print("")
except ModuleNotFoundError:
    print(
        "ERROR - Activate virtual environment before attempting to run driver script."
    )
    sys.exit(1)


class ArgParser(argparse.ArgumentParser):
    """Custom argument parser instance."""

    def error(self, message):
        """Custom Error Message."""
        sys.stderr.write(f"\nError: {message}\n\n")
        self.print_help()
        sys.exit(2)


def main():
    """Run the CLI."""
    parser = ArgParser(
        prog="runner.py",
        description="""
        Pac-Man Solutions - Back-End: AI solutions to abstractions of Pac-Man levels.
        """,
    )

    parser.add_argument(
        "run_config",
        choices=["single", "flask", "analytics"],
        help="""
        single = Run single game,
        flask = Run the Flask dev server,
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
        case "single":
            game = GameManager(
                args.level, configuration=RunConfiguration.LOCAL, verbose=args.verbose
            )
            game.game_loop()
        case "flask":
            app.run(debug=True, port=5001)
        case "analytics":
            PacmanAnalytics(runs=args.runs)


if __name__ == "__main__":
    main()
