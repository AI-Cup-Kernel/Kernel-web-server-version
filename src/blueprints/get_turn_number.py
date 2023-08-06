
from flask import Blueprint , jsonify , current_app 
from components.game import Game

from tools.check_token import token_required
from tools.check_player import check_player


get_turn_number = Blueprint('get_turn_number',__name__)

main_game = current_app.config['main_game']

@get_turn_number.route('/get_turn_number',methods=['GET'])
@token_required
@check_player
def get_turn_number_func():
    return jsonify(main_game.turn_number),200