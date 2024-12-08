import customtkinter as ctk
from src.shared_state import shared_state
from src.tabs.Pic_A_Time.ui import ui_components
from src.utils.file_operations import browse_folder
from src.tabs.Settings.core import load_settings, change_appearance, change_color_theme, take_backup_switch, select_backup_folder

settings_file = load_settings()

def settings_tab_content(settings_tab):

    btns_frame = ui_components["btns_frame"]
    phone_images_tab = ui_components["phone_images_tab"]

    # Appearance Mode
    appearance_options_frame = ctk.CTkFrame(settings_tab)
    appearance_options_frame.pack(pady=20)

    appearance_label = ctk.CTkLabel(appearance_options_frame, text="      Appearance     ")
    appearance_label.pack(side="left", padx=5)

    # Variable for holding appearance mode
    appearance_mode = ctk.StringVar(value=load_settings()["current"]["appearance"])

    appearance_system = ctk.CTkRadioButton(appearance_options_frame, text="System", variable=appearance_mode, value="System",command=lambda: change_appearance(appearance_mode, btns_frame, phone_images_tab))
    appearance_system.pack(side="left", padx=5)

    appearance_dark = ctk.CTkRadioButton(appearance_options_frame, text="Dark", variable=appearance_mode, value="Dark",command=lambda: change_appearance(appearance_mode, btns_frame, phone_images_tab))
    appearance_dark.pack(side="left", padx=5)

    appearance_light = ctk.CTkRadioButton(appearance_options_frame, text="Light", variable=appearance_mode, value="Light",command=lambda: change_appearance(appearance_mode, btns_frame, phone_images_tab))
    appearance_light.pack(side="left", padx=5)



    # Color Theme
    color_options_frame = ctk.CTkFrame(settings_tab)
    color_options_frame.pack(pady=20)#grid(row=1, column=0)#

    color_theme_label = ctk.CTkLabel(color_options_frame, text="Color Theme\n(Requires restart)")
    color_theme_label.pack(side="left", padx=5)

    # Variable for holding color theme
    color_theme = ctk.StringVar(value=load_settings()["current"]["color_theme"])

    color_theme_blue = ctk.CTkRadioButton(color_options_frame, text="Blue", variable=color_theme, value="blue",command=lambda: change_color_theme(color_theme)) # Default
    color_theme_blue.pack(side="left", padx=5)

    color_theme_green = ctk.CTkRadioButton(color_options_frame, text="Green", variable=color_theme, value="green",command=lambda: change_color_theme(color_theme))
    color_theme_green.pack(side="left", padx=5)

    color_theme_dark_blue = ctk.CTkRadioButton(color_options_frame, text="Dark Blue", variable=color_theme, value="dark-blue",command=lambda: change_color_theme(color_theme))
    color_theme_dark_blue.pack(side="left", padx=5)


    # Backup options frame
    backup_options_frame = ctk.CTkFrame(settings_tab)
    backup_options_frame.pack(pady=20)

    # Backup switch label
    take_backup_label = ctk.CTkLabel(backup_options_frame, text="Take Backup")
    take_backup_label.pack(side="left", padx=5)

    # Take backups switch 
    switch_val = "on" if load_settings()["current"]["take_backup"] == "yes" else "off"
    backup_switch_var = ctk.StringVar(value=switch_val)
    backup_switch = ctk.CTkSwitch(
        backup_options_frame, 
        text="", 
        variable=backup_switch_var, 
        onvalue="on", 
        offvalue="off", 
        command=lambda: take_backup_switch(
            backup_switch_var.get(),
            backup_folder_entry,
            browse_backup_folder_btn,
            select_backup_folder_btn
        )
    )
    backup_switch.pack(side="left", padx=5)


    # Backup folder label
    backup_folder_label = ctk.CTkLabel(backup_options_frame, text="Backup folder")
    backup_folder_label.pack(side="left")

    backup_folder_entry = ctk.CTkEntry(backup_options_frame, placeholder_text=load_settings()["current"]["backup_folder"])
    backup_folder_entry.pack(side="left", padx=5)

    browse_backup_folder_btn = ctk.CTkButton(
        backup_options_frame,
        text="Browse",
        width=70,
        command=lambda: browse_folder(backup_folder_entry)
    )
    browse_backup_folder_btn.pack(side="left")

    select_backup_folder_btn = ctk.CTkButton(backup_options_frame, text="Select", width=70, command=lambda: select_backup_folder(backup_folder_entry.get()))
    select_backup_folder_btn.pack(side="left",padx=5)