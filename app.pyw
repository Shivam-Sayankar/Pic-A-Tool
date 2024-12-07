from tkinter import *
import customtkinter as ctk
from src.tabs.Settings.core import load_settings
from src.tabs.Pic_A_Time.ui import pic_a_time_content
from src.tabs.Settings.ui import settings_tab_content

settings_file = load_settings()

root = ctk.CTk()
root.title("Pic-A-Tool")
root.geometry("907x750")
root.resizable(False, False)
# root.iconify()
# root.iconbitmap("assets/icon.ico")

# icon = PhotoImage(file="/assets/icon.png")
# root.iconphoto(True, icon)

ctk.set_appearance_mode(settings_file["current"]["appearance"])
ctk.set_default_color_theme(settings_file["current"]["color_theme"])

# Tabview
tabview = ctk.CTkTabview(root)
tabview.pack(fill="both", expand=True, padx=20, pady=20)

# Tabs
pic_a_time_tab = tabview.add("Pic-A-Time")
pic_a_name_tab = tabview.add("Pic-A-Name")
pic_a_tool_tab = tabview.add("Pic-A-Tool")
settings_tab = tabview.add("Settings")


pic_a_time_content(pic_a_time_tab)
settings_tab_content(settings_tab)

root.mainloop()