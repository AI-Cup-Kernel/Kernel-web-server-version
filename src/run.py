"""
    in this file we will make a server to run the game
    and add different APIs from blueprints to the server
"""



from flask import Flask
from blueprints.index import index
from blueprints.get_token import login
import importlib.util

# import the read_config function from tools/read_config.py
spec = importlib.util.spec_from_file_location('read_config', 'src/tools/read_config.py')
read_config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(read_config)


app = Flask(__name__)

# set the secret key
app.config['SECRET_KEY'] = 'your-secret-key'

# read the config file
config = read_config.read_config()

# register the blueprints
app.register_blueprint(index)
app.register_blueprint(login)


if __name__ == "__main__":
    app.run(debug=True, host=config['host'], port=config['port'])