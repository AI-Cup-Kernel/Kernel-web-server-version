# author: Mohamad Mahdi Reisi
# Date: 2023/8/16

# Description: This file is used to manage the turns of the game
# it will be called after the game is started


import time
from turn_controllers.start_turn import turn_request, end
from turn_controllers.check_finish import check_finish


def change_turn(main_game):
    while True:
        # increase the turn number 
        player_id = main_game.start_turn()
        print("start turn:", main_game.turn_number)

        # request the player to play
        resp = turn_request(player_id, main_game)

        # wait for the player to play
        time.sleep(main_game.config["turn_time"])
        if resp == -1:
            continue

        main_game.end_turn()
        # announce the end of the turn to the player
        end(player_id, main_game)
      
        # check if the game is finished
        check_finish(main_game)


