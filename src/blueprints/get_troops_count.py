from flask import Blueprint , jsonify , current_app 
from components.game import Game
from components.node import Node
from components.player import Player

from tools.check_token import token_required
from tools.check_player import check_player


get_troops_count = Blueprint('get_troops_count',__name__) 

main_game = current_app.config['main_game']

@get_troops_count.route('/get_troops_count',methods=['GET'])
@token_required
@check_player
def get_troops_count_func():
    output_dict = {}
    for node in main_game.list_of_nodes:
        output_dict[node.id]=node.number_of_troops
    return jsonify(output_dict),200