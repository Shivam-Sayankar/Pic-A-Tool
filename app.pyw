from tkinter import *
import customtkinter as ctk
from src.tabs.Pic_A_Time.ui import pic_a_time_content

root = ctk.CTk()
root.title("Pic-A-Tool")
root.geometry("907x750")
root.resizable(False, False)
# root.iconify()
# root.iconbitmap("assets/icon.ico")

# Tabview
tabview = ctk.CTkTabview(root)
tabview.pack(fill="both", expand=True, padx=20, pady=20)

# Tabs
pic_a_time_tab = tabview.add("Pic-A-Time")
pic_a_name_tab = tabview.add("Pic-A-Name")
pic_a_tool_tab = tabview.add("Pic-A-Tool")
settings_tab = tabview.add("Settings")


pic_a_time_content(pic_a_time_tab)

root.mainloop()