# author: Mohamad Mahdi Reisi
# Date: 2023/8/16

import json
import datetime

def check_finish(main_game):
    # check if the game is finished
    if main_game.turn_number >= int(main_game.config["number_of_turns"]):
        game_finished(main_game)

def game_finished(main_game):
    # finish the game
    # generate and save the main_game.log file into a json file in the log folder
    with open("log/" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".json", "w") as log_file:
        json.dump(main_game.log, log_file)
    
    main_game.finish_func()
