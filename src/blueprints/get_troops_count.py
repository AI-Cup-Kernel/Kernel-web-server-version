from flask import Blueprint , jsonify , current_app 
from src.tools.check_token import token_required
from src.tools.check_player import check_player

get_troops_count = Blueprint('get_troops_count',__name__) 

main_game = current_app.config['main_game']

@get_troops_count.route('/get_troops_count',methods=['GET'])
@token_required
@check_player
def get_troops_count_func(player_id):
    output_dict = {}
    for node in main_game.nodes.values():
        output_dict[node.id]=node.number_of_troops
    return jsonify(output_dict), 200