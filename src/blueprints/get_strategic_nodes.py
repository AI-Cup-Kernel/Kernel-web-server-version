from flask import Blueprint , jsonify , current_app 
from src.tools.check_token import token_required
from src.tools.check_player import check_player

get_strategic_nodes = Blueprint('get_strategic_nodes',__name__)

main_game = current_app.config['main_game']

@get_strategic_nodes.route('/get_strategic_nodes',methods=['GET'])
@token_required
@check_player
def get_strategic_nodes_func(player_id):
    output_dict={'strategic_nodes': [i.id for i in main_game.nodes.values() if i.is_strategic], 
                'score': [i.score_of_strategic for i in main_game.nodes.values() if i.is_strategic]}
    return jsonify(output_dict),200