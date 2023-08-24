from flask import Blueprint , jsonify , current_app 


next_state = Blueprint('next_state',__name__)

main_game = current_app.config['main_game']

@next_state.route('/next_state',methods=['GET'])
@current_app.config['token_required']
@current_app.config['check_player']
def next_state_func(player_id):
    if main_game.game_state != 2:
        output_dict={'error': 'The game is not in the turn state'}
        return jsonify(output_dict),400
    
    if main_game.state >= 4:
        output_dict={'error': 'you already finished the turn'}
        return jsonify(output_dict),400
    
    main_game.state += 1
    if main_game.debug:
        main_game.print("******* state changed to: " + str(main_game.state) + " *******") 

    output_dict={'game_state': main_game.state, 'message': 'success'}
    return jsonify(output_dict),200
