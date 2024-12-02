import os
import pickle
import time
from datetime import datetime
import tkinter as tk
from tkinter import filedialog
from src.utils.metadata_editor import extract_exif, apply_exif
from src.utils.pickle_helper import load_pickle
from src.components.progress_bar_manager import show_progress_bar, hide_progress_bar
from src.shared_state import shared_state
from pprint import pprint


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
        
        progress_bar.set(progress_bar.get() + step_size)
        progress_bar.update_idletasks()
    

    with open(backup_file_path, "wb") as backup_file:
        pickle.dump(backup_data, backup_file)


    backup_summary = (
        f"\n\nBackup created successfully at: {backup_file_path}\n"
        f"> Total Files Processed: {backup_data['backup_metadata']['total_files_processed']}\n"
        f"> Files with EXIF Data: {backup_data['backup_metadata']['files_with_exif_data']}\n"
        f"> Files without EXIF Data: {backup_data['backup_metadata']['files_without_exif_data']}\n\n"
    )

    preview_window.insert("end", backup_summary)
    preview_window.see(tk.END)

    time.sleep(1)

def restore_exif_data(preview_window, progress_bar, backup_file_path):
    
    try:

        # with open(backup_file_path, "rb") as backup_file:
        #     backup_data = pickle.load(backup_file)

        backup_data = load_pickle(backup_file_path)
        
        backup_file_name = backup_file_path.split("/")[-1]

        preview_window.insert("end", f"Backup file selected:\n\n\t{backup_file_name}\n\n")

        # Backup file format for reference
        """
            "backup_metadata": {
                "backup_date_time": backup_date_stamp,
                "original_path": images_folder,
                "total_files_processed": 0,
                "files_with_exif_data": 0,
                "files_without_exif_data": 0,
                "processed_by": PROCESSED_BY,
                "backup_type": backup_type
            },
            "files": {
                "file1": {
                    "exif_data": "<extracedted_exif_data>"
                }
            }
        """

        base = backup_data['backup_metadata']
        original_path = base['original_path']
        backup_info = (
            f"> Backup Date: {base['backup_date_time']}\n"
            f"> Original Path: {original_path}\n"
            f"> Backup Type: {base['backup_type']}\n"
            f"> Count of Backed up files: {base['total_files_processed']}\n"
        )

        preview_window.insert("end", backup_info)
        preview_window.see(tk.END)

        if not os.path.exists(original_path):
            preview_window.insert("end", "The original path of folder where images where stored does not exist.\n")
            original_path = filedialog.askdirectory(title="Select New Folder")


        # If original path is intact
        all_files = backup_data["files"].keys()
        total_files = len(all_files)

        base = backup_data['backup_metadata']

        # Progress bar setup
        progress_bar.set(1)
        step_size = 1 / total_files

        time.sleep(1)

        preview_window.insert("end", "\n*** Initialising Backup Restoration ***\n\n")

        for i, file in enumerate(all_files):
            # preview_window.insert("end", f"{file}\n")
            file_path = os.path.join(original_path, file)
            exif_data = backup_data["files"][file]["exif_data"]
            
            preview_window.insert("end", f"Restoring the Exif data for ({i+1}/{total_files}): {file}... ")

            try:
                apply_exif(file_path, exif_data)
                preview_window.insert("end", f"DONE\n")

            except Exception as e:
                preview_window.insert("end", f"\nCould not process {file}: {e}\n")

            finally:
                preview_window.see(tk.END)
                progress_bar.set(progress_bar.get() - step_size)
                progress_bar.update_idletasks()

    except Exception as e:
        preview_window.insert("end", f"Could not access the selected backupfile: {e}")

    