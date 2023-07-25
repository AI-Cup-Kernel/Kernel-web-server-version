'''
this is the most basic component of the Risk game.
each region is a node, and each node has a list of adjacent nodes in the main map
each node has an owner, which is a player object.
each player has it's own list of nodes that make a new map that is subgraph of the main map
'''

class Node:
    def __init__(self, id) -> None:
        self.id = id
        self.owner = None # Player object
        self.component_number = None # integer
        self.special_items = dict()
        self.adj_main_map = [] # list of Node objects
        self.adj_player_map = [] # list of Node objects  
