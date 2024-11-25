from utils.json_helpers import load_config
from utils.regex_helpers import matches
import tkinter as tk
from shared_state import shared_state
from pprint import pprint

config = load_config()

def phone_images_cat(selection, preview_window):

    if shared_state.pic_a_time["folder_selected"]:# folder_selected:

        preview_window.insert("end", f"Image Category Selected: {selection}\n")

        selection = "camera-image" if selection == "Camera-App Images" else "screenshot"
        shared_state.pic_a_time["image_category"] = selection
        


def phone_company_selection(selection, preview_window):

    if shared_state.pic_a_time["folder_selected"]:#.folder_selected:
        shared_state.pic_a_time["phone_company"] = selection
        preview_window.insert("end", f"Phone Company Selected: {selection} {format_and_sample()}\n")

        base = config["phones"][shared_state.pic_a_time["phone_company"]][shared_state.pic_a_time["image_category"]]

        all_matches = matches(
            shared_state.pic_a_time["folder_path"], 
            base["pattern"],
            preview_window
        )

        if len(all_matches) > 0:
            preview_window.insert("end", "\nPress the [ Modify ] button to proceed.\n")
            
        preview_window.see(tk.END)

    # print(f"phone comany selection function triggered. Selection: {selection}")

    # shared_state.pic_a_time["phone_company"] = selection
    # preview_window.insert("end", f"Phone Company Selected: {selection} {format_and_sample()}\n")
        

def format_and_sample():

    
    image_category = shared_state.pic_a_time["image_category"]
    phone_company = shared_state.pic_a_time["phone_company"]

    # print(f"company: {phone_company}, category: {image_category}")

    base = config["phones"][phone_company][image_category]
    # pprint(base)

    format = base["format"]
    sample = base["sample"]

    # preview_window.insert("end", f"[ {format} | {sample} ]")

    return f"\n\t[ {format} | {sample} ]"


def phone_company_dropdown_trigger(selection, preview_window):

    image_category = shared_state.pic_a_time["image_category"]
    phone_company = shared_state.pic_a_time["phone_company"]

    print(f"company: {phone_company}, category: {image_category}")

    base = config["phones"][shared_state.pic_a_time["phone_company"]][shared_state.pic_a_time["image_category"]]

    if shared_state.pic_a_time["folder_selected"]:
        phone_company_selection(
            selection, 
            preview_window
        )
        matches(
            shared_state.pic_a_time["folder_selected"], 
            base["pattern"],
            preview_window
        )

    