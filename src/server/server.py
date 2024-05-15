"""
File controlling the handling of the flask server and its routes.
"""

from flask import Flask
from flask import jsonify
from flask import redirect
from flask import request
from flask_cors import CORS
from src.exceptions import LevelNotFoundException
from src.services import game_manager
from src.services import level_handler

app = Flask(__name__)
cors = CORS(app, origins=["http://localhost:3000", "https://pacman.davidkidd.dev"])
app.config["CORS_HEADERS"] = "Content-Type"


@app.route("/")
def home():
    """Redirects the user to the API Documentation."""
    return redirect(
        "https://david-kidd.gitbook.io/ai-solutions-to-pac-man/the-api", 303
    )


@app.route("/get-levels", methods=["GET"])
def get_levels():
    """Returns an overview of information about all levels."""
    return jsonify(level_handler.get_overview()), 200


@app.route("/get-game", methods=["GET"])
def get_board():
    """Route to return a game simulation."""
    level_num = int(request.args.get("level_num"))  # type: ignore
    try:
        game = game_manager.GameManager(
            level_num, configuration=game_manager.RunConfiguration.SERVER
        )
        message = game.game_loop()
        status = 200
    except LevelNotFoundException as e:
        message = str(e)
        status = 400
    return jsonify(message), status


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=4000)
