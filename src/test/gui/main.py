import os
from tkinter import *
import customtkinter as ctk
from tkinter import filedialog
import json


folder_selected = False


def load_config():
    with open("data/main.json") as file:
        config = json.load(file)
    return config

def browse_folder():
    folder = filedialog.askdirectory()
    if folder:
        folder_path_entry_piati.delete(0, ctk.END)
        folder_path_entry_piati.insert(0, folder)


def preview_window_height(progressbar):
    return 240 if progressbar.winfo_ismapped() else 260


def change_appearance():
    selected_mode = appareance_mode.get()
    print(f"Selected Appearance Mode: {selected_mode}")
    ctk.set_appearance_mode(selected_mode)  # Change the theme dynamically
    btns_frame.configure(fg_color=phone_images_tab.cget("fg_color")) 


def change_color_theme():
    selected_mode = color_theme.get()
    print(f"Selected Color Theme: {selected_mode}")
    ctk.set_default_color_theme(selected_mode)  # Change the theme dynamically


def on_entry_change(event):
    current_text = folder_path_entry_piati.get()
    preview_window.insert("end", current_text)


def validate_path(string, textbox):

    global folder_selected

    if os.path.exists(string) and os.path.isdir(string):
        textbox.insert("end", f"Folder selected: {string}\n")
        folder_selected = True
    else:
        textbox.insert("end", f"Invalid Folder\n")


def phone_images_cat(selection):
    if folder_selected:
        preview_window.insert("end", f"Image Category Selected: {selection}\n")


def phone_company_selection(selection):
    if folder_selected:
        preview_window.insert("end", f"Phone Company Selected: {selection}\n")


# Set theme and colour options
ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green


root = ctk.CTk()
root.title("Pic-A-Tool")
root.geometry("907x750")
root.resizable(False, False)
# root.iconify()
# root.iconbitmap("assets/icon.ico")


# Tabs
tabview = ctk.CTkTabview(root)
tabview.pack(fill="both", expand=True, padx=20, pady=20)

pic_a_time_tab = tabview.add("Pic-A-Time")
pic_a_name_tab = tabview.add("Pic-A-Name")
pic_a_tool_tab = tabview.add("Pic-A-Tool")
settings_tab = tabview.add("Settings")



## Pic-A-Time Tab ## piati piana piato

# Header
header_piati = ctk.CTkLabel(pic_a_time_tab, text="Pic-A-Time", font=("Arial", 25, "bold"))
header_piati.pack(pady=25)

tagline_piati = ctk.CTkLabel(pic_a_time_tab, text="Update image timestamps based on their filenames", font=("Arial", 14))
tagline_piati.pack()


# Folder selection frame
folder_frame_piati = ctk.CTkFrame(pic_a_time_tab)
folder_frame_piati.pack(fill="x", padx=10, pady=15)

select_folder_lbl_piati = ctk.CTkLabel(folder_frame_piati, text="Select Folder")
select_folder_lbl_piati.pack(side="left", padx=5)

folder_path_entry_piati = ctk.CTkEntry(folder_frame_piati, placeholder_text="Enter folder path")
folder_path_entry_piati.pack(side="left", padx=10, fill="x", expand=True)
# folder_path_entry.bind("<KeyRelease>", on_entry_change)

browse_button_piati = ctk.CTkButton(folder_frame_piati, text="Browse", command=browse_folder)
browse_button_piati.pack(side="left")

select_folder_button = ctk.CTkButton(folder_frame_piati, text="Select Folder", command=lambda: validate_path(folder_path_entry_piati.get(), preview_window))
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

img_category_dropown = ctk.CTkComboBox(phone_images_tab, values=["Camera-App Images", "Screenshots"], command=phone_images_cat, width=270)
img_category_dropown.grid(row=0, column=1)

# Phone Company
img_category_label = ctk.CTkLabel(phone_images_tab, text="Phone Company")
img_category_label.grid(row=0, column=2, pady=10, padx=10)

config = load_config()
phone_companies = [config["phones"][key]["name"] for key in config["phones"].keys() if key != "regex-groups"]

img_category_dropown = ctk.CTkComboBox(phone_images_tab, values=phone_companies,command=phone_company_selection, width=270)
img_category_dropown.grid(row=0, column=3)


# Preview
preview_label = ctk.CTkLabel(phone_images_tab, text="Preview")#, fg_color="#565b5e")
preview_label.grid(row=1, column=0, columnspan=4, pady=10)

preview_window = ctk.CTkTextbox(phone_images_tab, width=800, height=240)
preview_window.grid(row=2, column=0, columnspan=4, padx=10)


# Confirmation buttons
btns_frame = ctk.CTkFrame(phone_images_tab, fg_color=phone_images_tab.cget("fg_color"))
btns_frame.grid(row=4, column=0, columnspan=4, pady=5)

# Progress bar
progressbar = ctk.CTkProgressBar(btns_frame, orientation="horizontal", width=800)
progressbar.set(0)
progressbar.pack(pady=14)

"""
# Functions to hide and show the widget
def hide_widget():
    label.pack_forget()  # Remove the widget from the layout

def show_widget():
    label.pack(pady=20)  # Re-add the widget to the layout
"""


modify_btn = ctk.CTkButton(btns_frame, text="Modify", height=40, width=150)
modify_btn.pack(side="left", pady=5)#, padx=70)#grid(row=3, column=1)

restore_btn = ctk.CTkButton(btns_frame, text="Restore", height=40, width=150)
restore_btn.pack(side="left", padx=175, pady=5)#grid(row=3, column=1)

cancel_btn = ctk.CTkButton(btns_frame, text="Cancel", height=40, width=150)
cancel_btn.pack(side="left", pady=5)#, padx=70)#grid(row=3, column=2)




## Pic-A-Name Tab ## - piana

# Header
header_piana = ctk.CTkLabel(pic_a_name_tab, text="Pic-A-Name", font=("Arial", 25, "bold"))
header_piana.pack(pady=25)

tagline_piana = ctk.CTkLabel(pic_a_name_tab, text="Rename images based on their timestamps", font=("Arial", 14))
tagline_piana.pack()

folder_frame_piana = ctk.CTkFrame(pic_a_name_tab)
folder_frame_piana.pack(fill="x", padx=20, pady=25)

select_folder_lbl_piana = ctk.CTkLabel(folder_frame_piana, text="Select Folder: ")
select_folder_lbl_piana.pack(side="left")

folder_path_entry_piana = ctk.CTkEntry(folder_frame_piana)
folder_path_entry_piana.pack(side="left", padx=10, fill="x", expand=True)

browse_button_piana = ctk.CTkButton(folder_frame_piana, text="Browse", command=browse_folder)
browse_button_piana.pack(side="left")




## Pic-A-Tool Tab ## - piato

# Header
header_piato = ctk.CTkLabel(pic_a_tool_tab, text="Pic-A-Tool", font=("Arial", 25, "bold"))
header_piato.pack(pady=25)

tagline_piato = ctk.CTkLabel(pic_a_tool_tab, text="More tools to manage and modify image metadata with ease.", font=("Arial", 14))
tagline_piato.pack()

folder_frame_piato = ctk.CTkFrame(pic_a_tool_tab)
folder_frame_piato.pack(fill="x", padx=20, pady=25)

lbl = ctk.CTkLabel(folder_frame_piato, text="Select Folder: ")
lbl.pack(side="left")

folder_path_entry_piato = ctk.CTkEntry(folder_frame_piato)
folder_path_entry_piato.pack(side="left", padx=10, fill="x", expand=True)

browse_button_piato = ctk.CTkButton(folder_frame_piato, text="Browse", command=browse_folder)
browse_button_piato.pack(side="left")




## SETTINGS TAB ##


# Appearance Mode
appearance_options_frame = ctk.CTkFrame(settings_tab)
appearance_options_frame.pack(pady=20)

appearance_label = ctk.CTkLabel(appearance_options_frame, text="     Appearance:     ")
appearance_label.pack(side="left", padx=5)

# Variable for holding appearance mode
appareance_mode = ctk.StringVar(value="System")

appareance_system = ctk.CTkRadioButton(appearance_options_frame, text="System", variable=appareance_mode, value="System",command=change_appearance)
appareance_system.pack(side="left", padx=5)

appareance_dark = ctk.CTkRadioButton(appearance_options_frame, text="Dark", variable=appareance_mode, value="Dark",command=change_appearance)
appareance_dark.pack(side="left", padx=5)


appareance_light = ctk.CTkRadioButton(appearance_options_frame, text="Light", variable=appareance_mode, value="Light",command=change_appearance)
appareance_light.pack(side="left", padx=5)



# Color Theme
color_options_frame = ctk.CTkFrame(settings_tab)
color_options_frame.pack(pady=20)#grid(row=1, column=0)#

color_theme_label = ctk.CTkLabel(color_options_frame, text="Color Theme:\n(Requires restart)")
color_theme_label.pack(side="left", padx=5)

# Variable for holding color theme
color_theme = ctk.StringVar(value="blue")

color_theme_blue = ctk.CTkRadioButton(color_options_frame, text="Blue", variable=color_theme, value="blue",command=change_color_theme)
color_theme_blue.pack(side="left", padx=5)

color_theme_green = ctk.CTkRadioButton(color_options_frame, text="Green", variable=color_theme, value="green",command=change_color_theme)
color_theme_green.pack(side="left", padx=5)


color_theme_dark_blue = ctk.CTkRadioButton(color_options_frame, text="Dark Blue", variable=color_theme, value="dark-blue",command=change_color_theme)
color_theme_dark_blue.pack(side="left", padx=5)


root.mainloop()