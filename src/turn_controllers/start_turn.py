# author: Mohamad Mahdi Reisi
# Date: 2023/8/16

# Description: This file is used to make a request to player_id to start its turn

import requests


def turn_request(player_id: int, main_game) -> None:
    # this function make a request to player_id to start its turn
    # return 1 if the request was successful
    # return -1 if the request was unsuccessful

    token = main_game.players[player_id].token
    port = main_game.players[player_id].port
    ip = main_game.players[player_id].ip

    # make a request to player_id to start its turn
    url = f'http://{ip}:{port}/turn'
    headers = {'x-access-token': token}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(response['error'])
    except:
        print(f"player{player_id} didn't response")
        return -1
    

    return 1
    