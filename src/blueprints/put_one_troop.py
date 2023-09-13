from flask import Blueprint , jsonify , current_app 
from flask import request

put_one_troop = Blueprint('put_one_troop',__name__)

main_game = current_app.config['main_game']

@put_one_troop.route('/put_one_troop',methods=['POST'])
@current_app.config['token_required']
@current_app.config['check_player']
def put_one_troop_func(player_id):
    # this API is used to put one troop on the map in the initial troop state of the game

    # body of the request should be like this:
    ## node_id: the id of the node that the player wants to put the troop on it

    # check if the player just put one Troop in a init turn
    if main_game.state != 1:
        return jsonify({'error':'You can not put more than one troop in a turn'}),400
    # check if the game is in the initial troop putting state
    if main_game.game_state != 1:
        return jsonify({'error':'The game is not in the initial troop putting state'}),400
    
    # check if the player has enough troops to put
    if main_game.player_turn.number_of_troops_to_place <= 0:
        return jsonify({'error':'You have no more initial troops to put'}),400
    
    # get the node_id from the request body
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

    # check the ownership status of the node
    if main_game.nodes[node_id].owner is None:
        # if the node is not owned by any player, add it to the player
        main_game.add_node_to_player(node_id, player_id)

    elif main_game.nodes[node_id].owner.id != player_id:
        return jsonify({'error':'This node is already owned by another player'}),400
    
    # add one troop to the node and subtract one from the player
    main_game.nodes[node_id].number_of_troops += 1
    main_game.player_turn.number_of_troops_to_place -= 1

    # add the node id and player id to the log variable of the game
    main_game.log_initialize.append([player_id, node_id])

    # change the state to 4 so player just can put one troop in a turn
    main_game.state = 6
    if main_game.debug:
        main_game.print(f"player {player_id} put one troop on node {node_id}")

    return jsonify({'message':'troop added successfully'}),200
