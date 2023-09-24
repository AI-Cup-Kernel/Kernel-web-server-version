from flask import Blueprint , jsonify , current_app 
from src.tools.check_token import token_required
from src.tools.check_player import check_player


get_state = Blueprint('get_state',__name__)

main_game = current_app.config['main_game']

@get_state.route('/get_state',methods=['GET'])
@token_required
@check_player
def get_state_func(player_id):
    output_dict={'state': main_game.state}
    return jsonify(output_dict),200