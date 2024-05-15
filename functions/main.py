from firebase_admin import initialize_app
from firebase_functions import https_fn
from firebase_functions import options
from flask import jsonify
from src.services import game_manager
from src.services import level_handler

app = initialize_app()


@https_fn.on_request(
    cors=options.CorsOptions(
        cors_origins="*",
        cors_methods=["get"],
    )
)
def get_levels(req: https_fn.Request) -> https_fn.Response:
    return jsonify(level_handler.get_overview())


@https_fn.on_request(
    cors=options.CorsOptions(
        cors_origins="*",
        cors_methods=["get"],
    )
)
def get_game(req: https_fn.Request) -> https_fn.Response:
    level_num = int(req.args.get("level_num"))  # type: ignore
    try:
        game = game_manager.GameManager(
            level_num, configuration=game_manager.RunConfiguration.SERVER
        )
        message = game.game_loop()
    except Exception as e:
        message = str(e)
    return jsonify(message)
