"""
in this API client shows that it's ready to start the game 
that means it has a server on the port that it said in the login API
"""

from flask import Blueprint
from flask import current_app
from flask import jsonify
import os

# get the main_game instance from the flask global variable
main_game = current_app.config['main_game']

# initialize the login blueprint
ready = Blueprint('ready', __name__)



@ready.route('/ready', methods=['GET'])
@current_app.config['token_required']
def ready_func(player_id):
    try:
        main_game.players[player_id].is_ready = True
        # disable proxy and vpn for the player IP 
        os.environ['NO_PROXY'] = main_game.players[player_id].ip
        output_dict = {"message": "every thing is ok, you should wait for other players to be ready"}
        main_game.check_all_players_ready()
        return jsonify(output_dict), 200

    except:
        output_dict = {"error": "this player_id doesn't exist"}
        return jsonify(output_dict), 404
