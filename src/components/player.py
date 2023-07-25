'''
each player has it's own list of nodes that make a new map
each player has an id and some special items

'''

class Player:
    def __init__(self, id) -> None:
        self.nodes = [] # list of Node objects that owned by this player
        self.id = id
        self.number_of_troops_to_place = 0 # integer
        self.special_items = dict()
    
    def eval_score(self) -> int:
        pass