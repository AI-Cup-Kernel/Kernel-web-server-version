from functools import wraps
from flask import current_app
from flask import request
from flask import jsonify
import jwt


def token_required(func):
    """
    This function is used as a decorator to check the token
    """

    # use wraps to keep the original function name
    @wraps(func)
    def decorator():
        token = None
        output_dict = dict()

        # ensure the jwt-token is passed with the headers
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token: # throw error if no token provided
            output_dict['error'] = 'Token is missing!'
            return jsonify(output_dict), 401

        # check if the token is valid and contains the player_id
        try:
           # decode the token to obtain user public_id
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            if data['player_id'] == None:
                raise Exception()     
        except:
            output_dict['error'] = 'Token is invalid!'
            return jsonify(output_dict), 401
        
        # call the function with the player_id
        return func(data['player_id'])
    return decorator
