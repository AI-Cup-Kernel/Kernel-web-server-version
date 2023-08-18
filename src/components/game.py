'''
game class contains all the components of the game
including the main map, players, and the game state and turn number
'''

from components.node import Node
from components.player import Player
from turn_controllers.change_turn import change_turn
import json
from flask import current_app
import threading
from tools.calculate_number_of_troops import calculate_number_of_troops


class Game:
    def __init__(self) -> None:

        self.players = {} # player_id: player object

        self.list_of_nodes = {} #  of Node objects

        self.turn_number = 0 # each turn is a round for a player to play
        self.state = 1 # that could be 'add troops': 1, 'attack': 2, 'move troops': 3
        self.player_turn = None # Player object: the player who is playing this turn
        self.game_started = False # True if the game already started
        self.game_state = 1 # 1: still need to initialize the troops, 2: the game started
        self.config = None # the config dictionary
        self.finish_func = None # the function that will be called when the game is finished

        # the following variables are used to for log file
        self.log_initialize = [] # save this list for the log file to show the initial troops of the players
        self.log_node_owner = []
        self.log_troop_count = []
        self.log_put_troop = []
        self.log_attack = []
        self.log_fortify = []

        self.log = {"initialize": self.log_initialize, "turns": {}}

    def update_game_state(self) -> None:
        # update the game state
        # check if the players has enough turn to put all their initial troops
        if self.game_state == 2:
            return
        if self.turn_number > int(self.config["number_of_players"]) * int(self.config["initial_troop"]):
            self.game_state = 2

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
            self.list_of_nodes[id] = node

        for edge in json_py["list_of_edges"]: 
                
            self.list_of_nodes[edge[0]].adj_main_map.append(self.list_of_nodes[edge[1]])
            self.list_of_nodes[edge[1]].adj_main_map.append(self.list_of_nodes[edge[0]])

    def check_all_players_ready(self) -> None:
        # check if the game started before or not
        if self.game_started == True:
            return
        
        # check if all players were logged in
        if len(self.players) != current_app.config['config']['number_of_players']:
            return
         
         # check if all players are ready
        for player in self.players.values():
            if not player.is_ready:
                return
            
        # Create a new thread for the change_turn function
        turn_thread = threading.Thread(target=change_turn, args=(self,))
        turn_thread.start()
        self.game_started = True

    def add_node_to_player(self, node_id, player_id):
        node_obj = self.list_of_nodes[node_id]
        player_obj = self.players[player_id]
        player_obj.nodes.append(node_obj)
        node_obj.owner = player_obj
        for i in node_obj.adj_main_map:
            if i.owner is not None and i.owner.id == player_id:
                i.adj_player_map.append(node_obj)
                node_obj.adj_player_map.append(i)
    
    def remove_node_from_player(self, node_id, player_id):
        node_obj = self.list_of_nodes[node_id]
        player_obj = self.players[player_id]
        player_obj.nodes.remove(node_obj)
        node_obj.owner = None
        for i in node_obj.adj_player_map:
            i.adj_player_map.remove(node_obj)

        node_obj.adj_player_map = []

    def start_turn(self):
        self.turn_number += 1
        player_id = self.turn_number % len(self.players)

        self.update_game_state()

        self.state = 1
        self.player_turn = self.players[player_id]
        self.player_turn.number_of_troops_to_place += calculate_number_of_troops(self.player_turn, self)

        if self.game_state == 2:
            self.log_node_owner = [i.owner.id if i.owner is not None else -1 for i in self.list_of_nodes.values()]
            self.log_troop_count = [i.number_of_troops for i in self.list_of_nodes.values()]
            self.log_put_troop = []
            self.log_attack = []
            self.log_fortify = []


        return player_id

    def end_turn(self):
        if self.game_state == 2:
            self.log['turns']['turn'+str(self.turn_number)] = {
                "nodes_owner": self.log_node_owner,
                "troop_count": self.log_troop_count,
                "add_troop": self.log_put_troop,
                "attack": self.log_attack,
                "fortify": self.log_fortify
            }
