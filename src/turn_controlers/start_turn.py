from flask import current_app
import requests


def turn_request(player_id: int, main_game) -> None:
    # this function make a request to player_id to start its turn
    token = main_game.players[player_id].token
    port = main_game.players[player_id].port
    ip = main_game.players[player_id].ip

    # make a request to player_id to start its turn
    url = f'http://{ip}:{port}/turn'
    headers = {'x-access-tokens': token}
    response = requests.get(url, headers=headers)
    counter = 1
    while response.status_code != 200:
        response = requests.get(url, headers=headers)
        counter += 1
        if counter > 10:
            print(f"player{player_id} didn't response")
    