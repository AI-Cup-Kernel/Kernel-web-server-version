import time
from turn_controlers.start_turn import turn_request

def change_turn(main_game):
    while True:
        print("start game")
        player_id = main_game.turn_number % len(main_game.players)
        turn_request(player_id, main_game)
        main_game.turn_number += 1
        time.sleep(1)

