from flask import Blueprint , jsonify , current_app 


get_turn_number = Blueprint('get_turn_number',__name__)

main_game = current_app.config['main_game']

@get_turn_number.route('/get_turn_number',methods=['GET'])
@current_app.config['token_required']
@current_app.config['check_player']
def get_turn_number_func(player_id):
    output_dict={'turn_number': main_game.turn_number}
    return jsonify(output_dict),200