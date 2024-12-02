import os # For working with directories
import piexif # For working with JPEG and TIFF
import pyexiv2 # For every other image format including PNG
from base64 import b64encode
from pprint import pprint


def format_exif_data(metadata):
    """Formats metadata into the desired EXIF format."""
    exif_data = {'0th': {}, '1st': {}, 'Exif': {}, 'GPS': {}, 'Interop': {}, 'thumbnail': None}

    # Iterate through EXIF keys and categorize
    for tag in metadata.exif_keys:
        value = metadata[tag].value
        tag_id = int(tag.split('.')[-1], 10)  # Extract the numeric part of the tag

        # Categorize the tags
        if tag.startswith("Exif.Image."):
            exif_data['0th'][tag_id] = value
        elif tag.startswith("Exif.Photo."):
            exif_data['Exif'][tag_id] = value
        elif tag.startswith("Exif.GPSInfo."):
            exif_data['GPS'][tag_id] = value
        elif tag.startswith("Exif.Interop."):
            exif_data['Interop'][tag_id] = value

    # Thumbnail extraction
    if metadata.thumbnail.has_thumbnail:
        exif_data['thumbnail'] = b64encode(metadata.thumbnail.data).decode('utf-8')

    return exif_data


def has_exif_data(file: str) -> bool:
    try:
        # Attempt to load EXIF data
        exif_data = piexif.load(file)
        
        # Checkign if the EXIF data contains any 0th, Exif, or other sections
        if exif_data.get("0th") or exif_data.get("Exif") or exif_data.get("GPS"):
            return True
        return False
    except piexif._exceptions.PiexifError:
        # If an error occurs (e.g., the image is not a valid EXIF file), return False
        return False


def extract_exif(file: str) -> dict:
    
    # if file.endswith(".jpg") or file.endswith(".jpeg") and has_exif_data(file):
    #     data = piexif.load(file)
    #     return data
    
    if file.endswith(".jpg") or file.endswith(".jpeg") and has_exif_data(file):
        try:
            exif_data = b64encode(piexif.load(file))
            
            # Convert binary thumbnail to Base64
            if exif_data.get("thumbnail"):
                exif_data["thumbnail"] = b64encode(exif_data["thumbnail"]).decode('utf-8')
            return exif_data
        except Exception as e:
            print(f"Failed to extract EXIF data: {e}")
            return None
    
    """
    else: # PNGs
        try:
            # Load the image metadata
            metadata = pyexiv2.ImageMetadata(file)
            metadata.read()

            # Format the EXIF data
            exif_data = format_exif_data(metadata)

            return exif_data
        except Exception as e:
            print(f"Failed to extract EXIF data: {e}")
            return None
    """
    


def apply_exif(file, exif_data):
    
    if file.endswith(".jpg") or file.endswith(".jpeg") and has_exif_data(file):
        piexif.remove(file)
        exif_bytes = piexif.dump(exif_data)
        piexif.insert(exif_bytes, file)
    
    """
    elif file.endswith(".png"):
        with pyexiv2.Image(file) as img:
            # Apply formatted EXIF data
            img.modify_exif(exif_data['0th'])
            img.modify_exif(exif_data['Exif'])
            img.modify_exif(exif_data['GPS'])
            img.modify_exif(exif_data['Interop'])

            # Add thumbnail if available (works only for JPEGs)
            if exif_data['thumbnail'] and img.mime_type == 'image/jpeg':
                img.thumbnail = exif_data['thumbnail']  # Add thumbnail

            # Save changes (automatically happens when exiting the 'with' block)
    """
    

    pprint(extract_exif(file))

