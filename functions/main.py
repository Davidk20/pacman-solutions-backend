"""The server scripts."""

from firebase_admin import initialize_app
from firebase_functions import https_fn, options
from flask import Flask, jsonify, request
from flask_cors import CORS

from functions.src.services import game_manager, level_handler

initialize_app()

app = Flask(__name__)
CORS(app)

approved = [
    r"pacman\.davidkidd\.dev",
    r"https://pacman\.davidkidd\.dev",
    r"https://pac-man-solutions\.web\.app",
]


@https_fn.on_request(
    cors=options.CorsOptions(
        cors_origins=approved,
        cors_methods=["get"],
    )
)
@app.get("/get_levels")
def get_levels(req: https_fn.Request = None) -> https_fn.Response:  # type: ignore
    # pylint: disable=unused-argument
    # requirement of cloud functions.
    """Return all levels as an overview."""
    return jsonify(level_handler.get_overview())


@https_fn.on_request(
    cors=options.CorsOptions(
        cors_origins=approved,
        cors_methods=["get"],
    )
)
@app.get("/get_game")
def get_game(req: https_fn.Request = None) -> https_fn.Response:  # type: ignore
    """Simulate a single game."""
    if req:
        level_num = int(req.args.get("level_num"))  # type: ignore
    else:
        level_num = int(request.args.get("level_num"))  # type: ignore
    try:
        game = game_manager.GameManager(
            level_num, configuration=game_manager.RunConfiguration.SERVER
        )
        message = game.game_loop()
    except Exception as e:  # pylint: disable=W0718
        message = str(e)
    return jsonify(message)
