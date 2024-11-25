
class SharedState:
    def __init__(self):

        self.pic_a_time = {
            "folder_selected": False,
            "folder_path": "",
            "image_category": "camera-image",
            "phone_company": None,
            "take_backup": True
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
