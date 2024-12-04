import os
import piexif
from pprint import pprint

folder = "/mnt/New Volume/Projects/pic-a-time-temp"

all_items = os.listdir(folder)

"""
 'IMG_20221125_111342.jpg',
 'IMG_20221212_161938.jpg',
 'IMG_20221212_161949.jpg',
"""

# pprint(all_items)

file_path = os.path.join(folder, "IMG_20221125_111342.jpg")
data = piexif.load(file_path)
print(data)