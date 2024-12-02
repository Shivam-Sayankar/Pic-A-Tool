from tkinter import *
import customtkinter as ctk


def show_progress_bar(progress_bar, preview_window, height_with_progress):
    progress_bar.pack(pady=14)
    progress_bar.set(0)
    preview_window.configure(height=height_with_progress)


def hide_progress_bar(progress_bar, preview_window, height_no_progress):
    progress_bar.pack_forget()
    preview_window.configure(height=height_no_progress)