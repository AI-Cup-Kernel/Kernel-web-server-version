# author: Mohamad Mahdi Reisi
# Date: 2023/8/16

# Description: This file is used to manage the turns of the game
# it will be called after all the players requested for ready


import time
from turn_controllers.start_turn import start_turn_request, end_turn_request
from turn_controllers.check_finish import check_finish


def change_turn(main_game):
    while True:
        # increase the turn number and initialize the turn
        player_id = main_game.start_turn()

        # add the turn number to the logs 
        if main_game.debug:
            print("start turn:", main_game.turn_number)
            main_game.print("--------- start turn: " + str(main_game.turn_number)+" ------------")

        # request the player to play
        resp = start_turn_request(player_id, main_game)

        # wait for the player to play
        time.sleep(main_game.config["turn_time"])

        # end the turn to add the logs for client
        main_game.end_turn()

        # announce the end of the turn to the player
        end_turn_request(player_id, main_game)
      
        # check if the game is finished
        check_finish(main_game)


