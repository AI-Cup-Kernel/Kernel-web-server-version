'''
game class contains all the components of the game
including the main map, players, and the game state and turn number
'''

import json
from node import Node


class Game:
    def __init__(self) -> None:
        self.list_of_players = [] # list of Player objects
        self.list_of_nodes = [] # list of Node objects
        self.state = None # that could be 'add troops': 1, 'attack': 2, 'move troops': 3
        self.turn_number = 0 # each turn is a round for a player to play
        self.player_turn = None # Player object: the player who is playing this turn
    
    def update_component_numbers(self) -> None:
        pass

    
    def read_map(self, map_file: str) -> None:
         
        with open(map_file,'r') as json_file:   #open jason file in to a json_file variable 
            
            json_py=json.load(json_file)        #load method converts json to dictionary in python 

        for id in range(1,json_py["number_of_nodes"]+1):

            node=Node(id)        #instance of node

            for edje in (json_py["list_of_edges"]): 
                
                if id in edje:  #find neighbors of id
                     node.adj_main_map.append(edje)

            self.list_of_nodes.append(node)