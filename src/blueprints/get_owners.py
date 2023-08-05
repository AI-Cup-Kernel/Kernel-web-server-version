

from flask import Blueprint , jsonify , current_app 
from components.game import Game
from components.node import Node
from components.player import Player

from tools.check_token import token_required
from tools.check_player import check_player


get_owners = Blueprint('get_owners',__name__) 

main_game = current_app.config['main_game']

@get_owners.route('/get_owners',methods=['GET'])
@token_required
@check_player
def get_owners_func():
    output_dict = {}
    for node in main_game.list_of_nodes:
        if node.owner!=None:
             output_dict[node.id] = node.owner.id
        else:
             output_dict[node.id] = -1
    return jsonify(output_dict),200