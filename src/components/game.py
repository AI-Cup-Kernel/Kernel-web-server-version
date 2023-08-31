# author: Mohamad Mahdi Reisi

# this is the main component of the game 
# it includes all the players and nodes of the game and all the information about the game

# turn state:
## 1: add troops
## 2: attack
## 3: move troops

# game state:
## 1: still need to initialize the troops (initial state)
## 2: the game started (turns state)


from src.components.node import Node
from src.components.player import Player
from src.turn_controllers.change_turn import change_turn
import json
from flask import current_app
import threading
from src.tools.calculate_number_of_troops import calculate_number_of_troops


class Game:
    def __init__(self) -> None:
        self.debug_logs = ""
        self.debug = False
        self.players = {} # player_id: player object, includes all players in the game

        self.nodes = {} # node_id: node object, includes all nodes of the map

        self.turn_number = 0 # each turn is a round for a player to play the game (it starts from 1)
        self.state = 1 # that could be 'add troops': 1, 'attack': 2, 'move troops': 3
        self.player_turn = None # Player object: the player who is playing this turn
        self.game_started = False # True if the game already started
        self.game_state = 1 # 1: still need to initialize the troops, 2: the game started
        self.config = None # the config dictionary
        self.finish_func = None # the function that will be called when the game is finished

        # the following variables are used to for log file
        self.log_initialize = [] # the log of the initialize phase 
        self.log_node_owner = [] # the log of the node owner at the beginning of each turn
        self.log_troop_count = [] # the log of the number of troops at the beginning of each turn
        self.log_put_troop = [] # the log of the number of troops that are put on the map at each turn
        self.log_attack = [] # the log of the attacks at each turn
        self.log_fortify = {} # the log of the move_troop at each turn
        self.log_fort = [] # the log of the fortify at each turn
        self.has_won_troop = False
        self.move_troop_done = False # a boolean that shows if the move_troop is done or not in the current turn
        # the main log file that will saved at the end of the game
        self.log = {"initialize": self.log_initialize, "turns": {}} 

    def update_game_state(self) -> None:
        # update the game state
        # this update will happen at the beginning of each turn

        # check if the the game is already in the turns state
        if self.game_state == 2:
            return
        
        # check if the players had enough turns to put all their initial troops
        if self.turn_number > int(self.config["number_of_players"]) * int(self.config["initial_troop"]):
            self.game_state = 2

    def add_player(self, player_id: int) -> None:
        # add a player to the game if it doesn't exist
        # this function will generate a new player object and add it to the players dictionary
        if player_id not in self.players:
            self.players[player_id] = Player(player_id)

    def read_map(self, map_file: str) -> None:
        # read the map from the json file and create the nodes and initialize them  

        # open the json file and load it into a dictionary
        with open(map_file,'r') as json_file:   
            json_py=json.load(json_file)        

        # create the nodes and add them to the nodes dictionary
        for id in range(json_py["number_of_nodes"]):
            node=Node(id)        
            self.nodes[id] = node

        # add edges to the nodes
        for edge in json_py["list_of_edges"]:  
            self.nodes[edge[0]].adj_main_map.append(self.nodes[edge[1]])
            self.nodes[edge[1]].adj_main_map.append(self.nodes[edge[0]])
        
        # add the strategic nodes to the nodes
        for id in json_py["strategic_nodes"]:
            self.nodes[id].is_strategic = True
        
        for i in range(len(json_py["scores_of_strategic_nodes"])):
            id = json_py["strategic_nodes"][i]
            score = json_py["scores_of_strategic_nodes"][i]
            self.nodes[id].score_of_strategic = score

    def check_all_players_ready(self) -> None:
        # this function will check if all players are ready to start the game
        # this function will be called after each player sends a ready request
        # this function also will start the game with a new thread if all players are ready

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
            
        # Create a new thread for start the game
        turn_thread = threading.Thread(target=change_turn, args=(self,))
        turn_thread.start()
        self.game_started = True

    def start_turn(self):
        # this function will be called at the beginning of each turn
        # it will initialize the turn variables in the game object

        # increase the turn number
        self.turn_number += 1

        # reset the move_troop_done variable
        self.move_troop_done = False

        # calculate the player who should play this turn
        player_id = self.turn_number % len(self.players)

        # check if the game needs to change state from initialize to turns
        self.update_game_state()

        # initialize the turn state to put troops for the player who should play this turn
        self.state = 1
        # initialize the player who should play this turn
        self.player_turn = self.players[player_id]
        self.has_won_troop = False
        # check if the game is in the turns state
        if self.game_state == 2:
            # calculate the number of troops that the player get at the beginning of this turn
            self.player_turn.number_of_troops_to_place += calculate_number_of_troops(player_id, self)
            # initialize the log variables
            ## the log of the node owner at the beginning of each turn
            self.log_node_owner = [i.owner.id if i.owner is not None else -1 for i in self.nodes.values()]
            ## the log of the number of troops at the beginning of each turn
            self.log_troop_count = [i.number_of_troops for i in self.nodes.values()]
            ## clear the log of the number of troops that are put on the map at each turn
            self.log_put_troop = []
            ## clear the log of the attacks at each turn
            self.log_attack = []
            ## clear the log of the move_troop at each turn
            self.log_fortify = {}

        return player_id

    def end_turn(self):
        # this function will be called at the end of each turn
        # it will save all the log variables in the main log variable

        # check if the game is in the turns state
        if self.game_state == 2:
            self.log['turns']['turn'+str(self.turn_number)] = {
                "nodes_owner": self.log_node_owner,
                "troop_count": self.log_troop_count,
                "add_troop": self.log_put_troop,
                "attack": self.log_attack,
                "fortify": self.log_fortify,
                "fort": [i.number_of_fort_troops for i in self.nodes.values()]
            }

    def print(self, text):
        # this function will print the text in the a log
        self.debug_logs += text + "\n"
    
    def add_node_to_player(self, node_id, player_id):
        self.players[player_id].nodes.append(self.nodes[node_id])
        self.nodes[node_id].owner = self.players[player_id]

    def remove_node_from_player(self, node_id, player_id):
        self.players[player_id].nodes.remove(self.nodes[node_id])
        self.nodes[node_id].owner = None