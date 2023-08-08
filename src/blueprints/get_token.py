"""
in this API each player will get a token, player_id, public_key, and port for running a server
client will use its server to know when its turn will start and when it should send its request to the server
token is used for authentication of the client 
client will use public to make the request comes from server not other clients
"""

from flask import Blueprint
from flask import current_app
from flask import jsonify
import jwt
from flask import request


# initialize the login blueprint
login = Blueprint('login', __name__)

# initialize the player_id
player_id = 1

# get the main_game instance from the flask global variable
main_game = current_app.config['main_game']



@login.route('/login', methods=['POST'])
def login_func():
    # get the token from the request body
    req = request.form.to_dict()
    if 'token' not in req:
        output_dict = {'error': 'token not found'}
        return jsonify(output_dict), 400
    player_token = req['token']
    # make sure there is no more than max_players players
    if player_id > current_app.config['config']['max_players']:
        output_dict = {'error': 'game players is full'}
        return jsonify(output_dict), 403

    # create a token for the player
    token = jwt.encode({'player_id': player_id}, current_app.config['SECRET_KEY'], 'HS256')

    # create the output dictionary
    output_dict = {'token': token, 'player_id': player_id, 'port': current_app.config['config']['client_port_start']+player_id}
    
    # initialize the player
    main_game.add_player(player_id)
    main_game.players[player_id].port = output_dict['port']
    main_game.players[player_id].ip = request.remote_addr
    main_game.players[player_id].token = player_token
    return jsonify(output_dict), 200


# This function will be called after login request successfully handled
@login.after_request
def after_request_func(response):
    global player_id
    # Check if the response was successful (status code 2xx)
    if 200 <= response.status_code < 300:
        # Increment the player_id
        player_id += 1
    return response
