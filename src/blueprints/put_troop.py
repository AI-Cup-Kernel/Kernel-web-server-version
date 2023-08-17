from flask import Blueprint , jsonify , current_app 
from components.game import Game
from flask import request

put_troop = Blueprint('put_troop',__name__)

main_game = current_app.config['main_game']

@put_troop.route('/put_troop',methods=['POST'])
@current_app.config['token_required']
@current_app.config['check_player']
def put_troop_func(player_id):

    # check if the game is in the initial troop putting state
    if main_game.game_state != 2:
        return jsonify({'error':'The game is not in the turn state'}),400
    
    if main_game.state != 1:
        return jsonify({'error':'The game is not in the troop putting state'}),400
    
    data = request.form.to_dict()
    if 'node_id' not in data:
        return jsonify({'error':'node_id is not provided'}),400
    
    try:
        node_id = int(data['node_id'])
    except:
        return jsonify({'error':'node_id is not valid it should be integer'}),400

    if node_id not in main_game.list_of_nodes.keys():
        return jsonify({'error':'node_id is not valid'}),400

    if 'number_of_troops' not in data:
        return jsonify({'error':'number_of_troops is not provided'}),400
    
    try:
        number_of_troops = int(data['number_of_troops'])
    except:
        return jsonify({'error':'number_of_troops is not valid it should be integer'}),400

    if main_game.player_turn.number_of_troops_to_place < number_of_troops:
        return jsonify({'error':'You do not have enough troops to place'}),400
    

    if main_game.list_of_nodes[node_id].owner is None:
        main_game.add_node_to_player(node_id, player_id)

    elif main_game.list_of_nodes[node_id].owner.id != player_id:
        return jsonify({'error':'This node is already owned by another player'}),400
    
    # add one troop to the node and subtract one from the player
    main_game.list_of_nodes[node_id].number_of_troops += number_of_troops
    main_game.player_turn.number_of_troops_to_place -= number_of_troops

    # add the node id and player id to the log variable of the game
    main_game.log_put_troop.append([node_id, number_of_troops])
    main_game.update_component_numbers()

    return jsonify({'message':'troop added successfully'}),200
