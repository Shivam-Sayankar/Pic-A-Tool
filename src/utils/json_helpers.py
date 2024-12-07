import json

def load_config():
    with open("src/config/main.v2.json") as file:
        config = json.load(file)
    return config