'''
read config file and return a dictionary
'''

import json

def read_config():
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config