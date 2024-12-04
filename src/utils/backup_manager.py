import os
import pickle
import time
from threading import Thread
from datetime import datetime
import tkinter as tk
from tkinter import filedialog
from src.utils.metadata_editor import extract_exif, apply_exif
from src.utils.pickle_helper import load_pickle
from src.utils.threads_helper import threaded_task
from src.components.progress_bar_manager import show_progress_bar, hide_progress_bar
from src.shared_state import shared_state
from pprint import pprint


APP_NAME = shared_state.app["app_name"]
APP_VERSION = shared_state.app["app_version"]
TAB_NAME = shared_state.pic_a_time["tab_name"]
PROCESSED_BY = f"{APP_NAME} v{APP_VERSION}"

def backup_exif_data(preview_window, progress_bar, images_folder: str, all_matches: list, backup_type: str):

    current_time = datetime.now()
    backup_file_name = current_time.strftime("%d-%b-%Y_%H-%M-%S")
    backup_date_stamp = current_time.strftime("%d-%b-%Y %H:%M:%S")

    root_backup_folder = shared_state.app["backup_folder"]
    backup_folder = os.path.join(root_backup_folder, TAB_NAME)  # backups/tab_name
    os.makedirs(backup_folder, exist_ok=True)

    backup_file_path = os.path.join(
        backup_folder, f"{backup_file_name}_[{TAB_NAME}].pkl"
        )  # backups/tab_name/backup_file_name_[TAB_NAME].pkl

    preview_window.see(tk.END)
    preview_window.insert("end", f"\n\nCreating Backup:  {backup_date_stamp}\n\n")


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
        
        # try:
        extract_output = extract_exif(file_path)
        exif_data = extract_output[0]
        extract_output_error = extract_output[1]
        # except Exception as e:
        #     preview_window.insert("end", f"Could not extract exif data of {file}: {e}\n")

        if exif_data:
            backup_data["backup_metadata"]["files_with_exif_data"] += 1
        else:
            preview_window.insert("end", f"Could not extract exif data of {file}: {extract_output_error}\n")
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

    # time.sleep(1)



# def threaded_backup_exif_data(preview_window, progress_bar, images_folder: str, all_matches: list, backup_type: str):

#     threaded_task(
#         backup_exif_data, 
#         preview_window, 
#         progress_bar, 
#         images_folder, 
#         all_matches, 
#         backup_type
#     )



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
            preview_window.insert("end", "Original folder not found. Please select a new folder to restore the files.\n\n")
            original_path = filedialog.askdirectory(title="Select New Folder for Restoration")


        # If original path is intact
        all_files = backup_data["files"].keys()
        total_files = len(all_files)

        base = backup_data['backup_metadata']

        # Progress bar setup
        progress_bar.set(1)

        if total_files > 0:
            step_size = 1 / total_files
        else:
            preview_window.insert("end", "No files to restore in the backup.\n")
            return

        time.sleep(1)

        preview_window.insert("end", "\n*** Initialising Backup Restoration ***\n\n")

        # Keeping a count of success and failures of processing
        successfully_processed = 0
        failed_to_process = 0
        failed_files = []

        for i, file in enumerate(all_files):
            # preview_window.insert("end", f"{file}\n")
            file_path = os.path.join(original_path, file)
            exif_data = backup_data["files"][file]["exif_data"]
            
            preview_window.insert("end", f"Restoring the Exif data for ({i+1}/{total_files}): {file}... ")

            try:
                apply_exif(file_path, exif_data)
                preview_window.insert("end", f"DONE\n")
                successfully_processed += 1

            except Exception as e:
                preview_window.insert("end", f"\nCould not process {file}: {e}\n")
                failed_to_process += 1
                failed_files.append(file)

            finally:
                preview_window.see(tk.END)
                progress_bar.set(progress_bar.get() - step_size)
                progress_bar.update_idletasks()
        
        restoration_summary = (
            f"\nRestoration complete.\n"
            f"> Total files processed: {successfully_processed}\n"
            f"> Failed to process: {failed_to_process} files\n"
        )

        preview_window.insert("end", restoration_summary)

        # Displaying files that couldnt be restored
        for img in failed_files:
            preview_window.insert("end", f"\t* {img}\n")
        
        failed_files = [] 

    except Exception as e:
        preview_window.insert("end", f"Could not access the selected backupfile: {e}\n\n")

    preview_window.see(tk.END)


def threaded_restore_exif_data(preview_window, progress_bar, backup_file_path):
    
    threaded_task(
        restore_exif_data,
        preview_window,
        progress_bar, 
        backup_file_path
    )