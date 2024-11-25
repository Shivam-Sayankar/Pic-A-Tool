import os
import re
import tkinter as tk
from pprint import pprint

def display_matches(all_matches, num,  preview_window):
    
    if len(all_matches) > 0:
        for i in range(num):
            preview_window.insert("end", f"\t{all_matches[i]}\n")

def matches(directory, pattern, preview_window):
    
    filename_pattern = re.compile(pattern)

    all_files = os.listdir(directory)
    all_matches = [file for file in all_files if (filename_pattern.search(file) and os.path.isfile(f"{directory}/{file}"))]

    pprint(all_files)

    display_limit = 10
    num = min( len(all_matches), display_limit )

    preview_window.insert("end", f"Total matches found: {len(all_matches)}\n\nDisplaying the first {num} matches (out of {len(all_matches)}):\n")

    preview_window.after(500, display_matches(all_matches, num, preview_window))

    preview_window.see(tk.END)

    return all_matches