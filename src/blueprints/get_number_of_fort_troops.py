from flask import Blueprint , jsonify , current_app 
from src.tools.check_token import token_required
from src.tools.check_player import check_player

get_number_of_fort_troops = Blueprint('get_number_of_fort_troops',__name__) 

main_game = current_app.config['main_game']

@get_number_of_fort_troops.route('/get_number_of_fort_troops',methods=['GET'])
@token_required
@check_player
def get_number_of_fort_troops_func(player_id):
    # this API used to get the number of fort troops on each node
    output_dict = {}
    for node in main_game.nodes.values():
        output_dict[node.id]=node.number_of_fort_troops
    return jsonify(output_dict), 200