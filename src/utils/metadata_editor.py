import os # For working with directories
import piexif # For working with JPEG and TIFF
import pyexiv2 # For every other image format including PNG
import tkinter as tk
from pprint import pprint


def extract_exif(file_path: str) -> dict:
    
    try:
        # Working with JPEGs
        if file_path.endswith(".jpg") or file_path.endswith("jpeg"):
            data = piexif.load(file_path)
            return data
    except Exception as e:
        print(f"Could not extract exif data because of: {e}")
        return None
    


def apply_exif(file_path, exif_data):
    
    # Working with JPEGs
    if file_path.endswith(".jpg") or file_path.endswith(".jpeg"):
        piexif.remove(file_path)
        exif_bytes = piexif.dump(exif_data)
        piexif.insert(exif_bytes, file_path)


def modify_exif_timestamp(preview_window, file_path, new_timestamp_text):
    file = file_path.split("/")[-1]
    if file_path.endswith(".jpg"):
        try:
            exif_dict = piexif.load(file_path)
            exif_dict['0th'][piexif.ImageIFD.DateTime] = new_timestamp_text
            exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = new_timestamp_text
            exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = new_timestamp_text

            piexif.remove(file_path)
            exif_bytes = piexif.dump(exif_dict)
            piexif.insert(exif_bytes, file_path)

            # print(f"Updated EXIF data for {file}")
            preview_window.insert("end", "DONE\n")
            preview_window.see(tk.END)

        except Exception as e:
            # preview_window.insert("end", f"\n⚠️ Failed to modify EXIF data for {file} ⚠️ : {e} \n")
            print(f"⚠️ Failed to modify EXIF data for {file} ⚠️ : {e}")
