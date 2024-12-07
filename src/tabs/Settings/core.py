import json

def load_settings():
    try:
        with open("src/config/settings.json") as file:
            settings = json.load(file)
    except FileNotFoundError:
        with open("src/config/settings.json", "w") as new_file:
            default_settings = {
                "default": {
                    "appearance" : "system",
                    "color_theme": "blue",
                    "take_backup": "yes",
                    "backup_folder": "src/backups/"
                }
            }
            settings = json.dump(default_settings, new_file, indent=4)

    return settings


def change_settings(key, value):
    
    settings_data = load_settings()

    with open("src/config/settings.json", "w") as file:
        settings_data["current"][key] = value
        json.dump(settings_data, file, indent=4)