# author: Mohamad Mahdi Reisi
# Date: 2023/8/16

# Description: This file is used to manage the turns of the game
# it will be called after the game is started


import time
from turn_controllers.start_turn import turn_request, end
from turn_controllers.check_finish import check_finish
from tools.calculate_number_of_troops import calculate_number_of_troops


def change_turn(main_game):
    while True:
        # increase the turn number 
        main_game.turn_number += 1
        print("start turn:", main_game.turn_number)

        # calculate the the player id of the current turn
        player_id = main_game.turn_number % len(main_game.players)
        
        # initialize the turn state and player object
        main_game.state = 1
        main_game.player_turn = main_game.players[player_id]
        main_game.player_turn.number_of_troops_to_place += calculate_number_of_troops(main_game.player_turn, main_game)
        
        # request the player to play
        resp = turn_request(player_id, main_game)

        # update the game state (state: turn or initial state)
        main_game.update_game_state()

        # wait for the player to play
        time.sleep(main_game.config["turn_time"])
        if resp == -1:
            continue

        # check if the game is finished
        check_finish(main_game)

        # announce the end of the turn to the player
        end(player_id, main_game)

