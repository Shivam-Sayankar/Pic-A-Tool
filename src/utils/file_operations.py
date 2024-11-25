import customtkinter as ctk
from tkinter import filedialog
import os
from shared_state import shared_state


def browse_folder(folder_path_entry):
    folder = filedialog.askdirectory()
    if folder:
        folder_path_entry.delete(0, ctk.END)
        folder_path_entry.insert(0, folder)


def validate_path(path, output_window):
    # global folder_selected
    if os.path.exists(path) and os.path.isdir(path):
        output_window.insert("end", f"Folder selected: {path}\n")
        shared_state.pic_a_time["folder_selected"] = True
        shared_state.pic_a_time["folder_path"] = path
    else:
        output_window.insert("end", f"Invalid Folder\n")