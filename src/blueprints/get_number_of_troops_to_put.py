from flask import Blueprint , jsonify , current_app 
from src.tools.check_token import token_required
from src.tools.check_player import check_player


get_number_of_troops_to_put = Blueprint('get_number_of_troops_to_put',__name__)

main_game = current_app.config['main_game']

@get_number_of_troops_to_put.route('/get_number_of_troops_to_put',methods=['GET'])
@token_required
@check_player
def get_number_of_troops_to_put_func(player_id):
    # return the number of troops that the player can put on the map
    output_dict={"number_of_troops": main_game.player_turn.number_of_troops_to_place}
    return jsonify(output_dict),200