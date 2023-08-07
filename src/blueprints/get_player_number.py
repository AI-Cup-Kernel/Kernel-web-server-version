from flask import Blueprint , jsonify , current_app 
from components.game import Game
from components.player import Player

from tools.check_token import token_required
from tools.check_player import check_player


get_player_number = Blueprint('get_player_number',__name__)

main_game = current_app.config['main_game']

@get_player_number.route('/get_player_number',methods=['GET'])
@token_required
@check_player
def get_player_number_func():
    output_dict={'player_number':main_game.player_turn.id}
    return jsonify(output_dict),200