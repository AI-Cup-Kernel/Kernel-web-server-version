"""
    this file will make a server 
    and add different APIs from blueprints to the server
"""

from flask import Flask
from components.game import Game
import tools.read_config as read_config
from flask import request
import os

debug = False

# read map file 
main_game = Game()
main_game.read_map('maps/map1.json')

# debugger for map
if debug:
    print("list of nodes: ")
    for i in range(len(main_game.list_of_nodes)):
        print([i.id for i in main_game.list_of_nodes[i].adj_main_map])
    print("end of list of nodes")

# initialize the flask app
app = Flask(__name__)
app.app_context().push()


# set the secret key
app.config['SECRET_KEY'] = 'your-secret-key'

# set the main_game instance in the flask global variable
app.config['main_game'] = main_game

# set the read_config function in the flask global variable
app.config['config'] = read_config.read_config()
main_game.config = app.config['config']

# set the game_finished function in the flask global variable
own_pid = os.getpid()
def kill_backend():
    os.kill(own_pid, 9)
    
main_game.finish_func = kill_backend


# set the debug variable in the flask global variable
app.config['debug'] = debug

# set the token_required and check_player functions in the flask global variable
from tools.check_token import token_required
from tools.check_player import check_player

app.config['token_required'] = token_required
app.config['check_player'] = check_player


# register the blueprints

# import blueprints
from blueprints.index import index
from blueprints.login import login
from blueprints.ready import ready
from blueprints.get_owners import get_owners
from blueprints.get_troops_count import get_troops_count
from blueprints.get_state import get_state
from blueprints.get_turn_number import get_turn_number
from blueprints.get_adj import get_adj
from blueprints.next_state import next_state
from blueprints.put_one_troop import put_one_troop

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

if __name__ == "__main__":
    app.run(debug=True, host=app.config['config']['host'], port=app.config['config']['port'])