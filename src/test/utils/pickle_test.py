import pickle
import piexif
from pprint import pprint

def extract_exif(file_path):
    data = piexif.load(file_path)
    return data

def exif_to_pickle(exif_data, backup_file_path):
    """
    Backs up EXIF data to a Pickle file.

    Args:
        exif_data: The EXIF data dictionary.
        backup_file_path: Path to save the Pickle backup file.
    """
    try:
        with open(backup_file_path, 'wb') as backup_file:
            pickle.dump(exif_data, backup_file)
        print(f"Backup successful: {backup_file_path}")
    except Exception as e:
        print(f"Error during backup: {e}")


def apply_exif(exif_data, file_path):    
    piexif.remove(file_path)
    exif_bytes = piexif.dump(exif_data)
    piexif.insert(exif_bytes, file_path)


file = "/media/shivammm/New Volume/Projects/Pic-A-Tool/src/test/sample-images/xiaomi/camera-images/IMG_20231015_100419.jpg"
data = extract_exif(file)
backup_file_name = "temp_backup.pkl"

pprint(data)

exif_to_pickle(data, backup_file_name)

with open(backup_file_name, "rb") as f:
    data = pickle.load(f)
    print("\n\ndata after applying:\n")    
    pprint(data)
    apply_exif(data, file)
