from tkinter import *
import customtkinter as ctk
from src.utils.file_operations import browse_folder, validate_path
from src.utils.json_helpers import load_config
from .core import phone_images_cat, phone_company_selection, threaded_modify_images, restore_images_exif
from src.shared_state import shared_state


def pic_a_time_content(pic_a_time_tab):

    ## Pic-A-Time Tab

    config = load_config()
    phone_companies = [key for key in config["phones"].keys() if key != "regex-groups"]

    # Header
    header = ctk.CTkLabel(pic_a_time_tab, text="Pic-A-Time", font=("Arial", 25, "bold"))
    header.pack(pady=25)

    tagline = ctk.CTkLabel(
        pic_a_time_tab, 
        text="Update image timestamps based on their filenames", 
        font=("Arial", 14)
        )
    tagline.pack()


    # Folder selection frame
    folder_frame = ctk.CTkFrame(pic_a_time_tab)
    folder_frame.pack(fill="x", padx=10, pady=15)

    select_folder_lbl = ctk.CTkLabel(folder_frame, text="Select Folder")
    select_folder_lbl.pack(side="left", padx=5)

    folder_path_entry = ctk.CTkEntry(folder_frame, placeholder_text="Enter folder path")
    folder_path_entry.pack(side="left", padx=10, fill="x", expand=True)

    browse_button = ctk.CTkButton(
        folder_frame, 
        text="Browse", 
        command=lambda: browse_folder(folder_path_entry)
        )
    browse_button.pack(side="left")

    select_folder_button = ctk.CTkButton(
        folder_frame, 
        text="Select Folder", 
        command=lambda: validate_path(folder_path_entry.get(), preview_window)
        )
    select_folder_button.pack(side="left", padx=10)

    # Options frame
    img_options_frame = ctk.CTkFrame(pic_a_time_tab)
    img_options_frame.pack(fill="x", padx=10, pady=10)

    # Image Category
    img_category_tabview = ctk.CTkTabview(img_options_frame)
    img_category_tabview.pack(fill="both", expand=True)

    phone_images_tab = img_category_tabview.add("Phones")
    camera_images_tab = img_category_tabview.add("Cameras")


    # Phone Image Category
    img_category_label = ctk.CTkLabel(phone_images_tab, text="Phone Image Category")
    img_category_label.grid(row=0, column=0, pady=10, padx=10)

    img_category_dropown = ctk.CTkComboBox(
        phone_images_tab, 
        values=["Camera-App Images", "Screenshots"], # Options to display
        command=lambda selection: phone_images_cat(
            selection,#("camera-image" if selection=="Camera-App Images" else "screenshots"), # Replacing the Display options with actual keys in json file
            preview_window,
            ),
        state="readonly",
        width=270
        )
    
    img_category_dropown.grid(row=0, column=1)

    # Phone Company
    img_category_label = ctk.CTkLabel(phone_images_tab, text="Phone Company")
    img_category_label.grid(row=0, column=2, pady=10, padx=10)

    
    phone_company_dropown = ctk.CTkComboBox(
        phone_images_tab, 
        values=phone_companies, 
        command=lambda selection: phone_company_selection(selection, preview_window),
        state="readonly", 
        width=270
        )
    phone_company_dropown.grid(row=0, column=3)


    # Preview Section
    preview_label = ctk.CTkLabel(phone_images_tab, text="Preview")
    preview_label.grid(row=1, column=0, columnspan=4, pady=10)

    preview_window_height = shared_state.pic_a_time["preview_height_no_progress"] # 270
    preview_window = ctk.CTkTextbox(phone_images_tab, width=800, height=240)#preview_window_height) # 240
    preview_window.grid(row=2, column=0, columnspan=4, padx=10)


    # Confirmation buttons
    btns_frame = ctk.CTkFrame(phone_images_tab, fg_color=phone_images_tab.cget("fg_color"))
    btns_frame.grid(row=4, column=0, columnspan=4, pady=5)

    # Progress bar
    progressbar = ctk.CTkProgressBar(btns_frame, orientation="horizontal", width=800)
    progressbar.set(0)
    progressbar.pack(pady=14)

    modify_btn = ctk.CTkButton(
        btns_frame,
        text="Modify",
        height=40,
        width=150,
        command=lambda: threaded_modify_images(
            preview_window, 
            progressbar
        )
    )
    modify_btn.pack(side="left", pady=5)

    restore_btn = ctk.CTkButton(
        btns_frame, 
        text="Restore", 
        height=40, 
        width=150,
        command=lambda: restore_images_exif(preview_window, progressbar)
    )
    restore_btn.pack(side="left", padx=175, pady=5)

    cancel_btn = ctk.CTkButton(btns_frame, text="Cancel", height=40, width=150)
    cancel_btn.pack(side="left", pady=5)



