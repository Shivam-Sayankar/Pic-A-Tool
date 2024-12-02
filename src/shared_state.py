
class SharedState:
    def __init__(self):

        self.app = {
            "app_name": "Pic-A-Tool",
            "app_version": "1.0",
            "take_backup": True,
            "backup_folder": "src/backups/"
        }

        self.pic_a_time = {
            "tab_name": "Pic-A-Time",
            "is_folder_selected": False,
            "folder_path": None,
            "image_category": "camera-image",
            "phone_company": None,
            "all_matches": [],
            "preview_height_with_progress": 240,
            "preview_height_no_progress": 270,

        }
        self.pic_a_name = {
            "folder_selected": False,
            "folder_path": "",
        }
        self.pic_a_tool = {
            "folder_selected": False,
            "folder_path": "",
        }

shared_state = SharedState()
