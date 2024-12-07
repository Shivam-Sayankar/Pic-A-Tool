import tkinter as tk
from tkinter import filedialog
import re
import os
import time
from src.utils.threads_helper import threaded_task
from src.utils.json_helpers import load_config
from src.utils.regex_helpers import matches
from src.utils.backup_manager import backup_exif_data, threaded_restore_exif_data
from src.utils.metadata_editor import modify_exif_timestamp
from src.shared_state import shared_state
from pprint import pprint

config = load_config()

def phone_images_cat(selection, preview_window):

    if shared_state.pic_a_time["is_folder_selected"]:

        preview_window.insert("end", f"Image Category Selected: {selection}\n")

        selection = "camera-image" if selection == "Camera-App Images" else "screenshot"
        shared_state.pic_a_time["image_category"] = selection
        


def phone_company_selection(selection, preview_window, progress_bar):

    if shared_state.pic_a_time["is_folder_selected"]:
        shared_state.pic_a_time["phone_company"] = selection
        shared_state.pic_a_time["cancel_request"] = False
        progress_bar.set(0)
        
        preview_window.insert("end", f"Phone Company Selected: {selection} {format_and_sample()}\n")

        base = config["phones"][shared_state.pic_a_time["phone_company"]][shared_state.pic_a_time["image_category"]]

        all_matches = matches(
            shared_state.pic_a_time["folder_path"], 
            base["pattern"],
            preview_window
        )

        shared_state.pic_a_time["all_matches"] = all_matches

        if len(all_matches) > 0:
            preview_window.insert("end", "\nPress the [ Modify ] button to proceed.\n")
        

def format_and_sample():
    
    image_category = shared_state.pic_a_time["image_category"]
    phone_company = shared_state.pic_a_time["phone_company"]
    base = config["phones"][phone_company][image_category]

    format = base["format"]
    sample = base["sample"]

    return f"\n\n\t[ {format}  |  {sample} ]"


def modify_images(preview_window, progress_bar):

    selected_folder = shared_state.pic_a_time["folder_path"]
    all_matches = shared_state.pic_a_time["all_matches"]

    image_category = shared_state.pic_a_time["image_category"]
    phone_company = shared_state.pic_a_time["phone_company"]
    pattern = config["phones"][phone_company][image_category]["pattern"]
    
    # Backup requirements
    take_backup = shared_state.app["take_backup"]

    if take_backup and len(all_matches) > 0:
        preview_window.insert("end", f"\nStarting backup...\n")
        backup_exif_data(preview_window, progress_bar, selected_folder, all_matches, "Pic-A-Time")
    elif len(all_matches) < 1:
        preview_window.insert("end", "\nNo Files to process\n")
        preview_window.see(tk.END)
        return


    preview_window.insert("end", f"\n*** Initialising process of modifying images ***\n\n")
    time.sleep(1)

    successfully_processed = 0
    failed_to_process = 0

    progress = 0
    progress_bar.set(progress)
    step_size = 1 / len(all_matches)

    for i, file in enumerate(all_matches):

        if shared_state.pic_a_time["cancel_request"]:
            preview_window.insert("end", f"\n\n~~ Image Modification Cancelled ~~\n\n")
            return
        
        filename_pattern = re.compile(pattern)
        match = filename_pattern.search(file)
        file_path = os.path.join(selected_folder, file)

        if os.path.isfile(file_path) and match:
            
            preview_window.insert("end", f"Processing ({i+1}/{len(all_matches)}) {file}... ")

            base = config["phones"]["regex-groups"]

            year = match.group(int(base["year"]))
            month = match.group(int(base["month"]))
            day = match.group(int(base["day"]))

            hour = match.group(int(base["hour"]))
            minute = match.group(int(base["min"]))
            second = match.group(int(base["sec"]))

            image_date_time_text = f"{year}:{month}:{day} {hour}:{minute}:{second}"
            # image_date_time_text = "2023:07:08 00:00:00"
            
            try:
                modify_exif_timestamp(preview_window, file_path, image_date_time_text)
                successfully_processed += 1
            except Exception as e:
                preview_window.insert("end", f"FAILED: {e}\n")
                failed_to_process += 1

            progress += step_size
            progress_bar.set(progress)
            progress_bar.update_idletasks()

            preview_window.see(tk.END)

    summary = (
        f"\n\n*** SUMMARY ***\n"
        f"> Successfully processed: {successfully_processed} files\n"
        f"> Failed to process: {failed_to_process} files\n"
    )

    preview_window.insert("end", summary)

    preview_window.see(tk.END)
    
    # progress_bar.set(0) # Reset back to zero


def threaded_modify_images(preview_window, progress_bar):

    threaded_task(
        modify_images,
        preview_window,
        progress_bar
    )

 
def restore_images_exif(preview_window, progress_bar, main_tab):

    # Initial backup directory
    initial_directory = shared_state.app["backup_folder"]
    
    # Selecting backup file
    backup_file_path = filedialog.askopenfilename(initialdir=initial_directory, title="Select a Backup File")

    preview_window.insert("end", "\n*** Restoration ***\n\n")

    threaded_restore_exif_data(preview_window, progress_bar, backup_file_path, main_tab)


def cancel_processes():
    shared_state.pic_a_time["cancel_request"] = True