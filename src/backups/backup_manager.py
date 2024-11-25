# from shared_state import shared_state
import os
import json
from datetime import datetime
from utils.metada_editor import extract_exif
from pprint import pprint

def backup_data(folder: str, all_matches: list, backup_folder="backup_data"):

    all_files = os.listdir(folder)
    # pprint(files)

    current_time = datetime.now()
    backup_file_name = current_time.strftime("%d-%b-%Y_%H-%M-%S")

    backup_metadata = {
        "backup_metadata": {
            "backup_date": backup_file_name,
            "total_files_processed": 0,
            "files_with_exif_data": 0,
            "files_without_exif_data": 0,
            "processed_by": "Pic-A-ToolKit v1.0"
        },
        "files": None
    }


    with open(f"{backup_folder}/{backup_file_name}.json", "w") as backfup_file:
        json.dump(backup_file_name, backup_metadata, indent=4)

    for file in all_files:
        if file in all_matches:
            file_path = os.path.join(folder, file)

            try:
                exif_data = extract_exif(file_path)

                backup_data_dict = {
                    backfup_file["files"]: {
                        file: {
                            "exif_data": exif_data,
                            "original_path": folder
                        }
                    }
                }

                
                int(backfup_file["backup_metadata"]["files_with_exif_data"]) += 1

                with open(f"{backup_folder}/{backup_file_name}.json", "a") as backup_file_again:
                    json.dump(backup_data_dict, backup_file_again, indent=4)
                    
            except Exception as e:
                print(e)
                int(backfup_file["backup_metadata"]["files_without_exif_data"]) += 1


            finally:
                int(backfup_file["backup_metadata"]["total_files_processed"]) += 1




def restore_data():
    pass

backup_data("/media/shivammm/New Volume/Projects/pic-a-time-temp/test/xiaomi/all-images")


{
    "backup_metadata": {
        "backup_date": "25-Nov-2024_22-53-32",
        "total_files_processed": 100,
        "files_with_exif_data": 80,
        "files_without_exif_data": 20,
        "processed_by": "Shivam's Metadata Tool v1.0"
    },
    "files": {
        "file1_name": {
            "exif_data": {
                "0th": {
                    "256": 1920,
                    "257": 1080
                },
                "Exif": {
                    "33434": 0.008,
                    "33437": 2.8
                },
                "GPS": {},
                "Interop": {},
                "thumbnail": None
            },
            "file_type": "JPEG",
            "last_modified": "2024-11-25T22:50:00",
            "original_path": "C:/path/to/file1.jpg"
        },
        "file2_name": {
            "exif_data": None,
            "file_type": "PNG",
            "last_modified": "2024-11-25T22:51:00",
            "original_path": "C:/path/to/file2.png"
        }
    }
}
