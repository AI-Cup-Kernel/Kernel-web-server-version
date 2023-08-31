from flask import Blueprint , jsonify , current_app 
from flask import request

fort = Blueprint('fort',__name__)

main_game = current_app.config['main_game']

@fort.route('/fort',methods=['POST'])
@current_app.config['token_required']
@current_app.config['check_player']
def fort_func(player_id):
    # this API used to apply the fortification ability of the player

    # the body of the request should be like this
    ## node_id : the id of the node that will be fortified
    ## troop_count : the number of troops that will be fortified

    # check if the Game is in the turn state
    if main_game.game_state != 2:
        return jsonify({'error':'The game is not in the turn state'}),400
    
    # check if the turn is in the fort state
    if main_game.state != 4:
        return jsonify({'error':'The game is not in the fort state'}),400

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
    # check if the node has an owner
    if main_game.nodes[node_id].owner is None:
        return jsonify({'error':'This node has no owner'}),400

    # check if the node is owned by the player
    if main_game.nodes[node_id].owner.id != player_id:
        return jsonify({'error':'This node is already owned by another player'}),400
    
    # check if the troop_count is provided
    if 'troop_count' not in data:
        return jsonify({'error':'troop_count is not provided'}),400
    
    # check if the troop_count is integer
    try:
        troop_count = int(data['troop_count'])
    except:
        return jsonify({'error':'troop_count is not valid it should be integer'}),400
    
    # check if the troop_count is valid
    if troop_count >= main_game.nodes[node_id].number_of_troops:
        return jsonify({'error':'there is not enough troops in the node'}),400

    # check if the player hasn't used the fortification ability in the game
    if main_game.player_turn.use_fort:
        return jsonify({'error':'you have already used the fortification ability in the game'}),400
    
    # start the fortification ability
    main_game.player_turn.use_fort = True

    # fortify the node
    main_game.nodes[node_id].number_of_troops -= troop_count
    main_game.nodes[node_id].number_of_fort_troops += main_game.config['fort_coef'] * troop_count

    if main_game.debug:
        main_game.print(f"player {player_id} fortified node {node_id} with {troop_count} troops")

    return jsonify({'success':'the fortification ability is applied successfully'}), 200