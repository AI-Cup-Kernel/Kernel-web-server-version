from flask import Blueprint , jsonify , current_app 
from flask import request
import random

attack = Blueprint('attack',__name__)

main_game = current_app.config['main_game']

@attack.route('/attack',methods=['POST'])
@current_app.config['token_required']
@current_app.config['check_player']
def attack_func(player_id):
    # this API used to attack a node from another node 

    # the body of the request should be like this
    ## attacking_id : the id of the node that will attack
    ## target_id : the id of the node that will be attacked
    ## fraction: the attack continues until the number of troops in the attacking node is fraction of the number of troops in the target node

    # check if the game is in the turn state
    if main_game.game_state != 2:
        return jsonify({'error':'The game is not in the turn state'}),400
    
    # check if the game is in the attack state
    if main_game.state != 2:
        return jsonify({'error':'The game is not in the attack state'}),400 

    # check the body of the request 
    data = request.form.to_dict()

    # check if the body has the attacking_id field
    if 'attacking_id' not in data:
        return jsonify({'error':'attacking_id is not provided'}),400
    
    # check if the attacking_id is integer
    try:
        attacking_id = int(data['attacking_id'])
    except:
        return jsonify({'error':'attacking_id is not valid it should be integer'}),400
    
    # check if the attacking_id is valid
    if attacking_id not in main_game.nodes.keys():
        return jsonify({'error':'attacking_id is not valid'}),400
    
    # check if the attacking_id has a owner
    if main_game.nodes[attacking_id].owner == None:
        return jsonify({'error':'attacking_id does not have any owner'}),400
    
    # check if the attacking_id is owned by the player
    if main_game.nodes[attacking_id].owner.id != player_id:
        return jsonify({'error':'attacking_id is not owned by the player'}),400

    # check if it has the target_id field
    if 'target_id' not in data:
        return jsonify({'error':'target_id is not provided'}),400
    
    # check if the target_id is integer
    try:
        target_id = int(data['target_id'])
    except:
        return jsonify({'error':'target_id is not valid it should be integer'}),400
    
    # check if the target_id is valid
    if target_id not in main_game.nodes.keys():
        return jsonify({'error':'target_id is not valid'}),400
    
    # check if the target_id has a owner
    if main_game.nodes[target_id].owner == None:
        return jsonify({'error':'target_id does not have any owner'}),400
    
    # check if the target_id is not owned by the player
    if main_game.nodes[target_id].owner.id == player_id:
        return jsonify({'error':'target_id is owned by the player'}),400
    
    # check if the body has the fraction field
    if 'fraction' not in data:
        return jsonify({'error':'fraction is not provided'}),400
    
    # check if the fraction is float
    try:
        fraction = float(data['fraction'])
    except:
        return jsonify({'error':'fraction is not valid it should be float'}),400
    

    # check if the player has at least 2 troops in the attacking node
    if main_game.nodes[attacking_id].number_of_troops < 2:
        return jsonify({'error':'attacking node does not have enough troops'}),400
    
    # check if the fraction is a positive number
    if fraction < 0:
        return jsonify({'error':'fraction should be positive'}),400

    attacker_troops = main_game.nodes[attacking_id].number_of_troops # number of troops in the attacking node
    target_troops = main_game.nodes[target_id].number_of_troops # number of troops in the target node

    while attacker_troops > 1 and target_troops > 0 and attacker_troops/target_troops > fraction:
        if attacker_troops > 3:
            attacker_dice = 3
        else:
            attacker_dice = attacker_troops - 1
        
        if target_troops >= 2:
            target_dice = 2
        else:
            target_dice = target_troops
        
        attacker_dice_list = []
        target_dice_list = []

        for _ in range(attacker_dice):
            attacker_dice_list.append(random.randint(1,6))
        for _ in range(target_dice):
            target_dice_list.append(random.randint(1,6))
        
        attacker_dice_list.sort(reverse=True)
        target_dice_list.sort(reverse=True)

        for i in range(min(attacker_dice,target_dice)):
            if attacker_dice_list[i] > target_dice_list[i]:
                target_troops -= 1
            else:
                attacker_troops -= 1
    

    # check if the attacker won
    if target_troops <= 0:
        main_game.nodes[attacking_id].number_of_troops = 1
        main_game.nodes[target_id].number_of_troops = attacker_troops - 1
        main_game.remove_node_from_player(target_id, main_game.nodes[target_id].owner.id)
        main_game.add_node_to_player(target_id, player_id)
        if main_game.player_turn.has_won_troop == False:
            main_game.player_turn.number_of_troops_to_place += main_game.config['number_of_troops_after_successful_attack']
            main_game.player_turn.has_won_troop = True

    else:
        main_game.nodes[attacking_id].number_of_troops = attacker_troops
        main_game.nodes[target_id].number_of_troops = target_troops



    log =  {
            "attacker": attacking_id,
            "target": target_id,
            "new_troop_count_attacker": main_game.nodes[attacking_id].number_of_troops,
            "new_troop_count_target": main_game.nodes[target_id].number_of_troops,
            "new_target_owner": main_game.nodes[target_id].owner.id
            }
    main_game.log_attack.append(log)

    return jsonify({'message':'attack is successful'}),200