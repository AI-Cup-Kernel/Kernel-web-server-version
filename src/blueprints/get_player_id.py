from flask import Blueprint , jsonify , current_app 
from src.tools.check_token import token_required
from src.tools.check_player import check_player


get_player_id = Blueprint('get_player_id',__name__)

main_game = current_app.config['main_game']

@get_player_id.route('/get_player_id',methods=['GET'])
@token_required
@check_player
def get_player_number_func(player_id):
    output_dict={'player_id': player_id}
    return jsonify(output_dict),200