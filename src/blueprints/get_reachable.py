from flask import Blueprint , jsonify , current_app 
from flask import request
from src.tools.find_reachable import find_reachable

get_reachable = Blueprint('get_reachable',__name__)

main_game = current_app.config['main_game']

@get_reachable.route('/get_reachable',methods=['POST'])
@current_app.config['token_required']
@current_app.config['check_player']
def get_reachable_func(player_id):
    # this API used to find all the nodes that the owner can move it's troops from node_id to them    
    # body of the request should be like this:
    ## node_id: the id of the node that the player wants to move his troops from it
    
    # check if the body of the request has node_id
    data = request.form.to_dict()

    if 'node_id' not in data:
        return jsonify({'error':'node_id is not provided'}),400
    
    # check if the node_id is integer
    try:
        node_id = int(data['node_id'])
    except:
        return jsonify({'error':'node_id is not valid it should be integer'}),400
    
    # check if the node_id is valid
    if node_id not in main_game.nodes.keys():
        return jsonify({'error':'node_id is not valid'}),400
    

    output_dict = {"reachable":find_reachable(node_id,main_game)}

    return jsonify(output_dict),200

