import json

def load_config():
    with open("config/main.v2.json") as file:
        config = json.load(file)
    return config

def display_options_to_keys(display_option):
    pass