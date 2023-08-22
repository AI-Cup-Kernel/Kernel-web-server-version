from functools import wraps
from flask import current_app
from flask import jsonify

main_game = current_app.config['main_game']

def check_player(func):
    @wraps(func)
    def decorator(player_id): 
        if main_game.game_started == False:
            return jsonify({"error":"The game didn't start yet"}),400
          
        if player_id != main_game.player_turn.id:
            return jsonify({"error":"It's not your turn"}),403
             
        return func(player_id)
    
    return decorator