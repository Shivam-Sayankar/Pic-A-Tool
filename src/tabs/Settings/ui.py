import customtkinter as ctk
from src.shared_state import shared_state
from src.tabs.Pic_A_Time.ui import ui_components
from src.tabs.Settings.core import load_settings, change_settings

settings_file = load_settings()

def settings_tab_content(settings_tab):

    btns_frame = ui_components["btns_frame"]
    phone_images_tab = ui_components["phone_images_tab"]

    def change_appearance():
        selected_mode = appareance_mode.get()
        print(f"Selected Appearance Mode: {selected_mode}")
        ctk.set_appearance_mode(selected_mode)  # Change the theme dynamically
        btns_frame.configure(fg_color=phone_images_tab.cget("fg_color")) 
 
        change_settings("appearance", selected_mode)


    def change_color_theme():
        selected_mode = color_theme.get()
        print(f"Selected Color Theme: {selected_mode}")
        ctk.set_default_color_theme(selected_mode)  # Change the theme dynamically

        change_settings("color_theme", selected_mode)


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

    color_theme_blue = ctk.CTkRadioButton(color_options_frame, text="Blue", variable=color_theme, value="blue",command=change_color_theme) # Default
    color_theme_blue.pack(side="left", padx=5)

    color_theme_green = ctk.CTkRadioButton(color_options_frame, text="Green", variable=color_theme, value="green",command=change_color_theme)
    color_theme_green.pack(side="left", padx=5)

    color_theme_dark_blue = ctk.CTkRadioButton(color_options_frame, text="Dark Blue", variable=color_theme, value="dark-blue",command=change_color_theme)
    color_theme_dark_blue.pack(side="left", padx=5)


    # Take backups switch 