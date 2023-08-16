# author: Mohamad Mahdi Reisi
# Date: 2023/8/16

# Description: This file is used to manage the turns of the game
# it will be called after the game is started


import time
from turn_controllers.start_turn import turn_request

def change_turn(main_game):
    while True:
        print("start turn:", main_game.turn_number)
        player_id = main_game.turn_number % len(main_game.players)
        resp = turn_request(player_id, main_game)
        main_game.turn_number += 1
        if resp == -1:
            continue
        time.sleep(1)

