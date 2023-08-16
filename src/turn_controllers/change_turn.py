# author: Mohamad Mahdi Reisi
# Date: 2023/8/16

# Description: This file is used to manage the turns of the game
# it will be called after the game is started


import time
from turn_controllers.start_turn import turn_request
from turn_controllers.check_finish import check_finish, game_finished

def change_turn(main_game):
    while True:
        
        main_game.turn_number += 1
        print("start turn:", main_game.turn_number)
        player_id = main_game.turn_number % len(main_game.players)
        main_game.state = 1
        main_game.player_turn = main_game.players[player_id]
        resp = turn_request(player_id, main_game)
        check_finish(main_game)

        if resp == -1:
            continue
        time.sleep(1)

