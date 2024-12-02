# from shared_state import shared_state
import os
import pickle
from datetime import datetime
import tkinter as tk
from utils.metadata_editor import extract_exif
from components.progress_bar_manager import show_progress_bar, hide_progress_bar
from shared_state import shared_state
from pprint import pprint
import time

APP_NAME = shared_state.app["app_name"]
APP_VERSION = shared_state.app["app_version"]
TAB_NAME = shared_state.pic_a_time["tab_name"]
PROCESSED_BY = f"{APP_NAME} v{APP_VERSION}"

def backup_exif_data(preview_window, progress_bar, images_folder: str, all_matches: list, backup_type: str, root_backup_folder="backups"):

    # all_files = os.listdir(images_folder)
    # pprint(files)

    current_time = datetime.now()
    backup_file_name = current_time.strftime("%d-%b-%Y_%H-%M-%S")
    backup_date_stamp = current_time.strftime("%d-%b-%Y %H:%M:%S")


    backup_folder = os.path.join(root_backup_folder, TAB_NAME)  # backups/tab_name
    os.makedirs(backup_folder, exist_ok=True)

    backup_file_path = os.path.join(
        backup_folder, f"{backup_file_name}_[{TAB_NAME}].pkl"
        )  # backups/tab_name/backup_file_name_[TAB_NAME].pkl

    preview_window.see(tk.END)
    preview_window.insert("end", f"\n\nCreating Backup:  {backup_date_stamp}")


    backup_data = {
        "backup_metadata": {
            "backup_date_time": backup_date_stamp,
            "original_path": images_folder,
            "total_files_processed": 0,
            "files_with_exif_data": 0,
            "files_without_exif_data": 0,
            "processed_by": PROCESSED_BY,
            "backup_type": backup_type
        },
        "files": {}
    }

    
    # Show progress bar
    # preview_window_height = shared_state.pic_a_time["preview_height_with_progress"]
    # show_progress_bar(progress_bar, preview_window, preview_window_height)

    progress = 0
    progress_bar.set(progress)

    step_size = 1 / len(all_matches)


    for file in all_matches:
        file_path = os.path.join(images_folder, file)

        if not os.path.isfile(file_path):
            preview_window.insert("end", f"\nSkipping {file}: File does not exist.")
            continue
        
        try:
            exif_data = extract_exif(file_path)
        except Exception as e:
            preview_window.insert("end", f"Could not extract exif data because of: {e}")

        if exif_data:
            backup_data["backup_metadata"]["files_with_exif_data"] += 1
        else:
            backup_data["backup_metadata"]["files_without_exif_data"] += 1

        backup_data["files"][file] = {
            "exif_data": exif_data
        }

        backup_data["backup_metadata"]["total_files_processed"] += 1
        
        # progress += step_size
        # progress_bar.set(progress)
        # time.sleep(1)
        progress_bar.set(progress_bar.get() + step_size)
        progress_bar.update_idletasks()
    

    with open(backup_file_path, "wb") as backup_file:
        pickle.dump(backup_data, backup_file)


    backup_summary = (
        f"\n\nBackup created successfully at: {backup_file_path}\n"
        f"Total Files Processed: {backup_data['backup_metadata']['total_files_processed']}\n"
        f"Files with EXIF Data: {backup_data['backup_metadata']['files_with_exif_data']}\n"
        f"Files without EXIF Data: {backup_data['backup_metadata']['files_without_exif_data']}\n\n"
    )

    preview_window.insert("end", backup_summary)
    preview_window.see(tk.END)

    # Hide progress bar
    # preview_window_height = shared_state.pic_a_time["preview_height_no_progress"]
    # hide_progress_bar(progress_bar, preview_window, preview_window_height)


def restore_data():
    pass