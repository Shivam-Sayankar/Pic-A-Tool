import customtkinter as ctk
import json
import os

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



def change_appearance(appareance_mode, btns_frame, phone_images_tab):
    selected_mode = appareance_mode.get()
    print(f"Selected Appearance Mode: {selected_mode}")
    ctk.set_appearance_mode(selected_mode)  # Change the theme dynamically
    btns_frame.configure(fg_color=phone_images_tab.cget("fg_color")) 

    change_settings("appearance", selected_mode)


def change_color_theme(color_theme):
    selected_mode = color_theme.get()
    print(f"Selected Color Theme: {selected_mode}")
    ctk.set_default_color_theme(selected_mode)  # Change the theme dynamically

    change_settings("color_theme", selected_mode)


def take_backup_switch(backup_switch_var, backup_folder_entry, browse_backup_folder_btn, select_backup_folder_btn):
    
    if backup_switch_var == "on":
        change_settings("take_backup", "yes")
        backup_folder_entry.configure(state="normal")
        browse_backup_folder_btn.configure(state="normal")
        select_backup_folder_btn.configure(state="normal")
        
    else:
        change_settings("take_backup", "no")
        backup_folder_entry.configure(state="disabled")
        browse_backup_folder_btn.configure(state="disabled")
        select_backup_folder_btn.configure(state="disabled")


def select_backup_folder(folder_path):

    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        change_settings("backup_folder", folder_path)