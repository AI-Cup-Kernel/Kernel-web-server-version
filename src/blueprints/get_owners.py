from flask import Blueprint , jsonify , current_app 


get_owners = Blueprint('get_owners',__name__) 

main_game = current_app.config['main_game']

@get_owners.route('/get_owners',methods=['GET'])
@current_app.config['token_required']
@current_app.config['check_player']
def get_owners_func(player_id):
    output_dict = {}
    for node in main_game.nodes.values():
        if node.owner!=None:
             output_dict[node.id] = node.owner.id
        else:
             output_dict[node.id] = -1
    return jsonify(output_dict),200