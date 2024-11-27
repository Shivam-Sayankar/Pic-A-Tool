import os # For working with directories
import piexif # For working with JPEG and TIFF
import pyexiv2 # For every other image format including PNG
import re # For file name identification
import json # working the the json file
from datetime import datetime
from pprint import pprint


with open("main.json", "r") as file:
    configs = json.load(file)
    # pprint(configs)

# pprint(configs)

WELCOME_TEXT = """
*** WELCOME TO PIC-A-TIME ***

A tool that changes your image's 
"Date Created" property based on their names
"""

INITIAL_OPTIONS = """
OPTIONS:
    1. Phone pictures (camera images or screenshots)
    2. Camera pictures
    3. Other
    4. Exit
"""

PHONE_IMAGE_CATEGORY = """
SELECT PICTURES CATEGORY:
    1. Camera images
    2. Screenshots    
"""


PHONE_COMPANY_OPTIONS = """
SELECT PHONE COMPANY/OS:
    1. Xiaomi
    2. Samsung
    3. AOSP Based custom ROMs
"""

CAMERA_OPTIONS = """
SELECT CAMERA OPTIONS:
    1. 
    2. 
"""


def display_phone_company_options():
    text = "\nSELECT PHONE COMPANY/OS:\n"
    for key in configs["phones"]:
        if key != "regex-groups":
            text += f'\t{key}. {configs["phones"][key]["name"]}\n'

    # return text
    print(text)


def modify_exif_of_jpeg(file_path, new_timestamp_text):
    file = file_path.split("/")[-1]
    try:
        exif_dict = piexif.load(file_path)
        exif_dict['0th'][piexif.ImageIFD.DateTime] = new_timestamp_text
        exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = new_timestamp_text
        exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = new_timestamp_text

        piexif.remove(file_path)
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, file_path)
        print(f"Updated EXIF data for {file}")
    except Exception as e:
        print(f"Failed to modify EXIF data for {file}: {e}")


def modify_file_timestamps(file_path, new_datetime_str):
    """
    Modifies the access and modification times of a file.

    Args:
        file_path (str): The path to the file.
        new_datetime_str (str): The new datetime string in the format "YYYY:MM:DD HH:MM:SS".
    """
    try:
        # Convert datetime string to a datetime object
        new_datetime_obj = datetime.strptime(new_datetime_str, "%Y:%m:%d %H:%M:%S")

        # Convert datetime object to a timestamp (seconds since epoch)
        timestamp = new_datetime_obj.timestamp()

        # Modify access and modification times
        os.utime(file_path, (timestamp, timestamp))

        print(f"Timestamps updated for {file_path}")
    except Exception as e:
        print(f"Failed to modify timestamps for {file_path}: {e}")


def process_phone_images(configs, folder, company_num, phone_option):
    
    # phone_option == camera-image / screenshot
    filename_pattern = re.compile(configs["phones"][company_num][phone_option])

    all_files = os.listdir(folder)
    all_matches = [file for file in all_files if filename_pattern.search(file)]

    if len(all_matches) > 0:
        confirmation = input(f"\nDo you confirm to modify {len(all_matches)} Xiaomi phone camera images? (y/n): ").lower()
        print()

        if confirmation == "y":

            for i in range(len(all_matches)):
                file = all_matches[i]

                match = filename_pattern.search(file)
                file_path = os.path.join(folder, file)

                if os.path.isfile(file_path) and match:
                    print(f"Processing ({i+1}/{len(all_matches)}) {file}...")

                    base = configs["phones"]["regex-groups"]

                    year = match.group(int(base["year"]))
                    month = match.group(int(base["month"]))
                    day = match.group(int(base["day"]))

                    hour = match.group(int(base["hour"]))
                    minute = match.group(int(base["min"]))
                    second = match.group(int(base["sec"]))

                    image_date_time_text = f"{year}:{month}:{day} {hour}:{minute}:{second}"
                    # image_date_time_text = "2023:07:08 00:00:00"

                    try:
                        modify_exif_of_jpeg(file_path, image_date_time_text)
                    except Exception as error:
                        print(f"\nCould not process {file} because of {error}")


def handle_phone_images(configs, image_folder_path):

    display_phone_company_options()
    
    company_num = input("Choose a phone company: ")
    if company_num in configs["phones"] and company_num != "regex-groups":

        print(PHONE_IMAGE_CATEGORY)
        phone_image_category = input("Enter phone image category (1/2): ")

        # camera clicks
        if phone_image_category == "1":
            process_phone_images(configs, image_folder_path, company_num, "camera-image")
        # screenshots
        elif phone_image_category == "2":
            process_phone_images(configs, image_folder_path, company_num, "screenshot")
        else:
            print("Invalid option.")

    else:
        print("Invalid option.")


print(WELCOME_TEXT)
image_directory = input("Where are your photos located? (folder path): ")


if os.path.exists(image_directory) == True:

    while True:
        print(INITIAL_OPTIONS)
        image_category = input("Select an option (1/2/3/4): ")

        # Phone Pictures
        if image_category == "1": #1. Phone pictures (camera images or screenshots)
            handle_phone_images(configs, image_directory)
            
        # Camera Pictures
        elif image_category == "2":
            # handle_phone_images(configs, image_directory)
            pass

        # Other/Older images
        elif image_category == "3":
            # handleOtherImages(image_directory)
            pass

        # Exit the program
        elif image_category == "4":
            break

        # Invalid command
        else:
            print("\nInvalid option")

else:
    print("\nInvalid path.")

# Exit message    
print("\nThanks for using Pic-A-Time! Have a good day! :)\n")