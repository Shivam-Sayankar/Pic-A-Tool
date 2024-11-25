from tkinter import *
import customtkinter as ctk
from tabs.Pic_A_Time.ui import pic_a_time_content

# Set theme and colour options
# ctk.set_appearance_mode("system")  # Modes: system (default), light, dark
# ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

# /media/shivammm/New Volume/Projects/pic-a-time-temp/test/xiaomi/all-images

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


pic_a_time_content(pic_a_time_tab)
# settings_tab_content(settings_tab)

root.mainloop()