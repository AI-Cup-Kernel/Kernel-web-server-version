from flask import Blueprint , jsonify , current_app 
from flask import request

printer = Blueprint('print',__name__)

main_game = current_app.config['main_game']

@printer.route('/printer',methods=['POST'])
@current_app.config['token_required']
@current_app.config['check_player']
def printer_func(player_id):
    # this API used for debugging


    # get text from the request body
    data = request.form.to_dict()

    # check if the text is provided
    if 'text' not in data:
        return jsonify({'error':'text is not provided'}),400
    
    text = str(data['text'])

    if main_game.debug:
        main_game.print(text)

    return jsonify({'message':'printed successfully'}),200
