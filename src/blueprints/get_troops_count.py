from flask import Blueprint , jsonify , current_app 


get_troops_count = Blueprint('get_troops_count',__name__) 

main_game = current_app.config['main_game']

@get_troops_count.route('/get_troops_count',methods=['GET'])
@current_app.config['token_required']
@current_app.config['check_player']
def get_troops_count_func(player_id):
    output_dict = {}
    for node in main_game.nodes.values():
        output_dict[node.id]=node.number_of_troops
    return jsonify(output_dict), 200