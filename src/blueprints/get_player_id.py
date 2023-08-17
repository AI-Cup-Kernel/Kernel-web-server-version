from flask import Blueprint , jsonify , current_app 



get_player_id = Blueprint('get_player_id',__name__)

main_game = current_app.config['main_game']

@get_player_id.route('/get_player_id',methods=['GET'])
@current_app.config['token_required']
@current_app.config['check_player']
def get_player_number_func(player_id):
    output_dict={'player_id': player_id}
    return jsonify(output_dict),200