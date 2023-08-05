from functools import wraps
from flask import current_app


main_game = current_app.config['main_game']

def check_player(func):
    @wraps(func)
    def decorator(player_id):   
        if player_id != main_game.player_turn.id:
            return "You are not allowed to do this action"
             
        return func(player_id)
    
    return decorator