from flask import Blueprint , jsonify , current_app 
from components.game import Game


next_state = Blueprint('next_state',__name__)

main_game = current_app.config['main_game']

@next_state.route('/next_state',methods=['GET'])
@current_app.config['token_required']
@current_app.config['check_player']
def next_state_func(player_id):
    if main_game.state >= 3:
        output_dict={'error': 'you are in the last state'}
        return jsonify(output_dict),400
    main_game.state += 1
    output_dict={'game_state': main_game.state, 'message': 'success'}
    return jsonify(output_dict),200