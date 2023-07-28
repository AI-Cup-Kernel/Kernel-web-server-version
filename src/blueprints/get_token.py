from flask import Blueprint
from flask import current_app
from flask import jsonify
import jwt
import importlib.util


# import the read_config function from tools/read_config.py
spec = importlib.util.spec_from_file_location('read_config', 'src/tools/read_config.py')
read_config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(read_config)

# import main_game instance from components/game.py
spec = importlib.util.spec_from_file_location('main_game', 'src/components/game.py')
game = importlib.util.module_from_spec(spec)
spec.loader.exec_module(game)

# initialize the login blueprint
login = Blueprint('login', __name__)

# initialize the player_id
player_id = 1

# read the config file
config = read_config.read_config()


@login.route('/login', methods=['GET'])
def login_func():
    # make sure there is no more than max_players players
    if player_id > config['max_players']:
        output_dict = {'error': 'You are not allowed to login anymore'}
        return jsonify(output_dict), 403

    # create a token for the player
    token = jwt.encode({'player_id': player_id}, current_app.config['SECRET_KEY'], 'HS256')

    # create the output dictionary
    output_dict = {'token': token, 'player_id': player_id, 'public_key': game.main_game.public_key_encoded, 'port': config['client_port_start']+player_id}
    game.main_game.add_player(player_id)
    
    return jsonify(output_dict), 200


@login.after_request
def after_request_func(response):
    global player_id
    # Check if the response was successful (status code 2xx)
    if 200 <= response.status_code < 300:
        # Increment the player_id
        player_id += 1
    return response

