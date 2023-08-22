from flask import Blueprint , jsonify , current_app 
from flask import request

put_troop = Blueprint('put_troop',__name__)

main_game = current_app.config['main_game']

@put_troop.route('/put_troop',methods=['POST'])
@current_app.config['token_required']
@current_app.config['check_player']
def put_troop_func(player_id):
    # this API used to put troops in the map in the put troop state

    # body of the request should be like this:
    ## node_id: the id of the node that the player wants to put the troop on it
    ## number_of_troops: the number of troops that the player wants to put on the node

    # check if the game is in the turn state
    if main_game.game_state != 2:
        return jsonify({'error':'The game is not in the turn state'}),400

    # check if the turn in the put troop state
    if main_game.state != 1:
        return jsonify({'error':'The game is not in the troop putting state'}),400
    
    # get the node_id and number_of_troops from the request body
    data = request.form.to_dict()

    # check if the node_id is provided
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

    # check if the number_of_troops is provided
    if 'number_of_troops' not in data:
        return jsonify({'error':'number_of_troops is not provided'}),400
    
    # check if the number_of_troops is integer
    try:
        number_of_troops = int(data['number_of_troops'])
    except:
        return jsonify({'error':'number_of_troops is not valid it should be integer'}),400

    # check if the player has enough troops to place
    if main_game.player_turn.number_of_troops_to_place < number_of_troops:
        return jsonify({'error':'You do not have enough troops to place'}),400
    
    # check if the node is not owned by anyone
    if main_game.nodes[node_id].owner is None:
        main_game.add_node_to_player(node_id, player_id)

    # check if the node is not owned by another player
    elif main_game.nodes[node_id].owner.id != player_id:
        return jsonify({'error':'This node is already owned by another player'}),400
    
    # check if the number_of_troops is positive
    if number_of_troops <= 0:
        return jsonify({'error':'number_of_troops should be positive'}),400
    
    # add one troop to the node and subtract one from the player
    main_game.nodes[node_id].number_of_troops += number_of_troops
    main_game.player_turn.number_of_troops_to_place -= number_of_troops

    # add the node id and player id to the log variable of the game
    main_game.log_put_troop.append([node_id, number_of_troops])

    if main_game.debug:
        main_game.print("player " + str(player_id) + " put " + str(number_of_troops) + " troops on node " + str(node_id))

    return jsonify({'message':'troop added successfully'}),200
