import time
from flask import current_app


def change_turn(main_game):
    while True:
        print("start game")
        main_game.turn_number += 1
        time.sleep(1)
