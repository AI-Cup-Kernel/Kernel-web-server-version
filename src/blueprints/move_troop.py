from flask import Blueprint , jsonify , current_app 
from flask import request
from tools.find_path import find_path

move_troop = Blueprint('move_troop',__name__)

main_game = current_app.config['main_game']

@move_troop.route('/move_troop',methods=['POST'])
@current_app.config['token_required']
@current_app.config['check_player']
def move_troop_func(player_id):
    print("move___________")
    # check if the game is in the turn state
    if main_game.game_state != 2:
        return jsonify({'error':'The game is not in the turn state'}),400
    
    # check if the game is in the move troop state
    if main_game.state != 3:
        return jsonify({'error':'The game is not in the move troop state'}),400
    
    # check the body of the request 
    data = request.form.to_dict()

    # check if the body has the source field
    if 'source' not in data:
        return jsonify({'error':'source is not provided'}),400
    
    # check if the source is integer
    try:
        source = int(data['source'])
    except:
        return jsonify({'error':'source is not valid it should be integer'}),400
    
    # check if the source is valid
    if source not in main_game.list_of_nodes.keys():
        return jsonify({'error':'source is not valid'}),400
    
    # check if the source has a owner
    if main_game.list_of_nodes[source].owner == None:
        return jsonify({'error':'source does not have any owner'}),400

    # check if the source is owned by the player
    if main_game.list_of_nodes[source].owner.id != player_id:
        return jsonify({'error':'source is not owned by the player'}),400

    # check if it has the destination field
    if 'destination' not in data:
        return jsonify({'error':'destination is not provided'}),400
    
    # check if the destination is integer
    try:
        destination = int(data['destination'])
    except:
        return jsonify({'error':'destination is not valid it should be integer'}),400
    
    # check if the destination is valid
    if destination not in main_game.list_of_nodes.keys():
        return jsonify({'error':'destination is not valid'}),400
    
    # check if the destination has a owner
    if main_game.list_of_nodes[destination].owner == None:
        return jsonify({'error':'destination does not have any owner'}),400
    
    if main_game.list_of_nodes[destination].owner.id != player_id:
        return jsonify({'error':'destination is not owned by the player'}),400
    
    if 'troop_count' not in data:
        return jsonify({'error':'troop_count is not provided'}),400
    
    try:
        troop_count = int(data['troop_count'])
    except:
        return jsonify({'error':'troop_count is not valid it should be integer'}),400

    # check if the player has at least 2 troops in the source node
    if main_game.list_of_nodes[source].number_of_troops <= troop_count:
        return jsonify({'error':'source node does not have enough troops'}),400
    
    # check if there is a path between source and destination
    res, path = find_path(source,destination,main_game,player_id)
    if not res:
        return jsonify({'error':'there is no path between source and destination'}),400
    
    main_game.list_of_nodes[source].number_of_troops -= troop_count
    main_game.list_of_nodes[destination].number_of_troops += troop_count

    main_game.state = 4

    main_game.log_fortify = [troop_count, path]

    return jsonify({'message':'troops moved successfully'}),200