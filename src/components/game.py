'''
game class contains all the components of the game
including the main map, players, and the game state and turn number
'''

import rsa

class Game:
    def __init__(self) -> None:
        self.list_of_players = [] # list of Player objects
        self.list_of_nodes = [] # list of Node objects
        self.state = None # that could be 'add troops': 1, 'attack': 2, 'move troops': 3
        self.turn_number = 0 # each turn is a round for a player to play
        self.player_turn = None # Player object: the player who is playing this turn
        # Generate key pair (public key and private key)
        (public_key, self.private_key) = rsa.newkeys(512)
        # Encode the public key to send it to the server
        self.public_key_encoded = public_key.save_pkcs1().decode('utf-8')

    def update_component_numbers(self) -> None:
        pass

    
    def read_map(self, map_file: str) -> None:
        pass



main_game = Game()

    
    