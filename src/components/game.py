'''
game class contains all the components of the game
including the main map, players, and the game state and turn number
'''

import rsa
from node import Node
import json

# import the Player class from components/player.py
import importlib.util
spec = importlib.util.spec_from_file_location('Player', 'src/components/player.py')
player = importlib.util.module_from_spec(spec)
spec.loader.exec_module(player)
Player = player.Player


class Game:
    def __init__(self) -> None:

        self.players = dict() # key: player_id, value: Player object

        self.list_of_nodes = [] # list of Node objects
        self.state = None # that could be 'add troops': 1, 'attack': 2, 'move troops': 3
        self.turn_number = 0 # each turn is a round for a player to play
        self.player_turn = None # Player object: the player who is playing this turn
        # Generate key pair (public key and private key)
        (public_key, self.private_key) = rsa.newkeys(512)
        # Encode the public key to send it to the server
        self.public_key_encoded = public_key.save_pkcs1().decode('utf-8')

    def add_player(self, player_id: int) -> None:
        # add a player to the game if it doesn't exist
        if player_id not in self.players:
            self.players[player_id] = Player(player_id)

    def update_component_numbers(self) -> None:
        pass

    
    def read_map(self, map_file: str) -> None:
                 
        with open(map_file,'r') as json_file:   #open jason file in to a json_file variable 
            
            json_py=json.load(json_file)        #load method converts json to dictionary in python 

        for id in range(json_py["number_of_nodes"]):

            node=Node(id)        #instance of node
            self.list_of_nodes.append(node)

        for edje in (json_py["list_of_edges"]): 
                
            self.list_of_nodes[edje[0]].adj_main_map.append(edje)
            self.list_of_nodes[edje[1]].adj_main_map.append(edje)

    
    def check_all_players_ready(self) -> None:
        pass

main_game = Game()

    
    