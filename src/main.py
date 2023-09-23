# author: Mohamad Mahdi Reisi

# this is the main file of the game that will run the game
# this file reads the map file and creates a game object and initializes it
# then make a server
# and add different APIs from blueprints to the server
# it also has a function to kill the server

from flask import Flask
from src.components.game import Game
import src.tools.read_config as read_config
import os
import requests
import argparse
import logging


# define argument parser
parser = argparse.ArgumentParser(description='choose map to play on')
parser.add_argument('-m', '--map', type=str, help='choose map to play on')
args = parser.parse_args()


# read map file 
main_game = Game()

# ask player to choose map from the list of maps
maps = os.listdir('maps')

## get the selected map from the player
selected_map = str(maps.index(args.map)) if args.map != None else "None"

while selected_map.isdigit() == False or int(selected_map) >= len(maps) or int(selected_map) < 0:
    ## show the list of maps from the maps folder
    print("Choose a map from the list of maps:")
    for i, map in enumerate(maps):
        print(i,'-', map)
    selected_map = input("Enter the number of the map you want to choose: ")

## read the selected map
main_game.read_map('maps/'+maps[int(selected_map)])


# initialize the flask app
app = Flask(__name__)
app.app_context().push()


#disable flask logs
if True:
    app.logger.propagate = False
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

# set the secret key
app.config['SECRET_KEY'] = 'your-secret-key'

# set the main_game instance in the flask global variable
app.config['main_game'] = main_game

# set the read_config function in the flask global variable
app.config['config'] = read_config.read_config()
main_game.config = app.config['config']

# set the debug variable to True or False to see the debug messages and generate debug logs 
debug = app.config['config']['debug']

# set the game_finished function in the flask global variable
own_pid = os.getpid()
def kill_backend():
    # kill the backend process
    if debug:
        print("killing the backend process")
    for player in main_game.players.values():
        try:
            requests.get('http://'+player.ip+':'+str(player.port)+'/kill', headers={'x-access-token': player.token}, timeout=0.1)
        except:
            pass
    os.kill(own_pid, 9)
    
main_game.finish_func = kill_backend


# set the debug variable in the flask global variable
app.config['debug'] = debug
main_game.debug = debug

# set the token_required and check_player functions in the flask global variable
from src.tools.check_token import token_required
from src.tools.check_player import check_player

app.config['token_required'] = token_required
app.config['check_player'] = check_player


# register the blueprints

# import blueprints
from src.blueprints.index import index
from src.blueprints.login import login
from src.blueprints.ready import ready
from src.blueprints.get_owners import get_owners
from src.blueprints.get_troops_count import get_troops_count
from src.blueprints.get_state import get_state
from src.blueprints.get_turn_number import get_turn_number
from src.blueprints.get_adj import get_adj
from src.blueprints.next_state import next_state
from src.blueprints.put_one_troop import put_one_troop
from src.blueprints.put_troop import put_troop
from src.blueprints.get_player_id import get_player_id
from src.blueprints.attack import attack
from src.blueprints.move_troop import move_troop
from src.blueprints.get_strategic_nodes import get_strategic_nodes
from src.blueprints.get_number_of_troops_to_put import get_number_of_troops_to_put
from src.blueprints.get_reachable import get_reachable
from src.blueprints.get_number_of_fort_troops import get_number_of_fort_troops
from src.blueprints.fort import fort
from src.blueprints.printer import printer

## a blueprint for the test server
app.register_blueprint(index)

## a blueprint for the login API(get token, player_id, public_key, port for the client)
app.register_blueprint(login)

## a blueprint for the ready API
app.register_blueprint(ready)

## a blueprint for the get owners API
app.register_blueprint(get_owners)

## a blueprint for the get troops count API
app.register_blueprint(get_troops_count)

## a blueprint for the get state API
app.register_blueprint(get_state)

## a blueprint for the get turn number API
app.register_blueprint(get_turn_number)

## a blueprint for the get adj API
app.register_blueprint(get_adj)

## a blueprint for the next state API
app.register_blueprint(next_state)

## a blueprint for the put one troop API
app.register_blueprint(put_one_troop)

## a blueprint for the put troop API
app.register_blueprint(put_troop)

## a blueprint for the get player id API
app.register_blueprint(get_player_id)

## a blueprint for the attack API
app.register_blueprint(attack)

## a blueprint for the move troop API
app.register_blueprint(move_troop)

## a blueprint for the get strategic nodes API
app.register_blueprint(get_strategic_nodes)

## a blueprint for the get number of troops to put API
app.register_blueprint(get_number_of_troops_to_put)

## a blueprint for the get reachable API
app.register_blueprint(get_reachable)

## a blueprint for the get number of fort troops API
app.register_blueprint(get_number_of_fort_troops)

## a blueprint for the fort API
app.register_blueprint(fort)

## a blueprint for the print API
app.register_blueprint(printer)

# run the server
app.run(debug=False, host=app.config['config']['host'], port=app.config['config']['port'])