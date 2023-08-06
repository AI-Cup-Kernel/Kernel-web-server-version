'''
game class contains all the components of the game
including the main map, players, and the game state and turn number
'''

from components.node import Node
from components.player import Player
from turn_controlers.change_turn import change_turn
import json
from flask import current_app
import threading


class Game:
    def __init__(self) -> None:

        self.players = {} # player_id: player object

        self.list_of_nodes = [] # list of Node objects

        self.turn_number = 0 # each turn is a round for a player to play
        self.state = None # that could be 'add troops': 1, 'attack': 2, 'move troops': 3
        self.player_turn = None # Player object: the player who is playing this turn
        self.game_started = False # True if the game already started
        self.game_state = 1 # 1: still need to initialize the troops, 2: the game started

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
                
            self.list_of_nodes[edje[0]].adj_main_map.append(self.list_of_nodes[edje[1]])
            self.list_of_nodes[edje[1]].adj_main_map.append(self.list_of_nodes[edje[0]])

    
    def check_all_players_ready(self) -> None:
        # check if the game started before or not
        if self.game_started == True:
            return
        
        # check if all players were logged in
        if len(self.players) != current_app.config['config']['max_players']:
            return
         
         # check if all players are ready
        for player in self.players.values():
            if not player.is_ready:
                return
            
        # Create a new thread for the change_turn function
        turn_thread = threading.Thread(target=change_turn, args=(self,))
        turn_thread.start()
        self.game_started = True

    
    