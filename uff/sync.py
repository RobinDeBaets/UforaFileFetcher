import os
import threading

from uff.brightspace import BrightspaceAPI
from uff.files import download_files


def sync(config):
    brightspace_api = BrightspaceAPI.from_config(config)
    output_dir = os.path.expanduser(config["output_directory"])
    for course_id in config["courses"]:
        print(f"Syncing {course_id}")
        thread = threading.Thread(target=download_files, args=(brightspace_api, course_id, output_dir))
        thread.start()
