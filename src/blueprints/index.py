from flask import Blueprint

index = Blueprint('index', __name__)

@index.route('/', methods=['GET'])
def index_func():
    return "Welcome to Risk Game!"