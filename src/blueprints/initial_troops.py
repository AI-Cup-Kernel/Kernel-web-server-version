"""
in this file we define a API for the initial troops placement
each player should put one troop in its turn 
player can just put troops in its own territory or a territory that doesn't have a owner 
"""

from flask import Blueprint, current_app, jsonify, request
import requests

from tools.check_token import token_required
from tools.check_player import check_player

init_troop = Blueprint('init_troop', __name__)

@init_troop.route('/init_troop', methods=['POST'])
@token_required
@check_player
def init_troop_func(current_user):
    return "init_troop"
