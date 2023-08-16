
from flask import Blueprint , jsonify , request , current_app
from components.game import Game


put_x_troops_in_region_y = Blueprint('put_x_troops_in_region_y',__name__)

main_game = current_app.config['main_game']

@put_x_troops_in_region_y.route('/put_x_troops_in_region_y',methods=['POST'])

@current_app.config['token_required']
@current_app.config['check_player']

def put_x_troops_in_region_y_func(player_id):
    if main_game.state != 1:
        output_dict = {'error':'the game is not in initializing troops state'}
        return jsonify(output_dict),400
    else:
        if request.form.get('region') == None or \
        (not request.form.get('region').isdigit()) or\
        int(request.form.get('region')) < 0 or \
        int(request.form.get('region')) >= len(main_game.list_of_nodes):
            output_dict = {'error':'the region is invalid'}
            return jsonify(output_dict),400
        if request.form.get('number_of_troops') == None or \
        (not request.form.get('number_of_troops').isdigit()) or \
        int(request.form.get('number_of_troops')) == 0:
            output_dict = {'error':'the number_of_troops is invalid'}
            return jsonify(output_dict),400
        else:
            index_of_region = int(request.form.get('region')) 
            if main_game.list_of_nodes[index_of_region].owner != None and \
            main_game.list_of_nodes[index_of_region].owner.id != main_game.player_turn.id:
                output_dict = {'error':'you are not allowed to put troops in this region'}
                return jsonify(output_dict),400
            else:
                number_of_troops = int(request.form.get('number_of_troops'))
                if main_game.player_turn.number_of_troops_to_place < number_of_troops:
                    output_dict = {'error':"you don't have enough troops"}
                    return jsonify(output_dict),400
                else:
                    main_game.list_of_nodes[index_of_region].number_of_troops += number_of_troops
                    main_game.player_turn.number_of_troops_to_place -= number_of_troops
                    output_dict = {'success':'troops were placed in the desired region'}
                    return jsonify(output_dict),200