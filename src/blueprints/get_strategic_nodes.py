from flask import Blueprint , jsonify , current_app 
from components.game import Game



get_strategic_nodes = Blueprint('get_strategic_nodes',__name__)

main_game = current_app.config['main_game']

@get_strategic_nodes.route('/get_strategic_nodes',methods=['GET'])
@current_app.config['token_required']
@current_app.config['check_player']
def get_strategic_nodes_func(player_id):
    output_dict={'strategic_nodes': [i.id for i in main_game.nodes if i.is_strategic]}
    return jsonify(output_dict),200