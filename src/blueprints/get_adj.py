from flask import Blueprint , jsonify , current_app 
from src.tools.check_token import token_required
from src.tools.check_player import check_player

get_adj = Blueprint('get_adj',__name__) 

main_game = current_app.config['main_game']

@get_adj.route('/get_adj',methods=['GET'])
@token_required
@check_player
def get_adj_func(player_id):
    # this API used to the list of the adjacent nodes of each node
    output_dict = {}
    for node in main_game.nodes.values():
        output_dict[str(node.id)]= [i.id for i in node.adj_main_map]
    return jsonify(output_dict), 200