# author: Mohamad Mahdi Reisi
# Date: 2023/8/16

def check_finish(main_game):
    # check if the game is finished
    if main_game.turn_number >= int(main_game.config["number_of_turns"]):
        game_finished(main_game)

def game_finished(main_game):
    # finish the game
    main_game.finish_func()
    exit()
