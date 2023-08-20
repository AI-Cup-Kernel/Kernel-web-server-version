from flask import Blueprint
from flask import jsonify
index = Blueprint('index', __name__)

@index.route('/', methods=['GET'])
def index_func():
    # this API used to check if the server is running
    return jsonify({"message":"Welcome, server is running"}), 200