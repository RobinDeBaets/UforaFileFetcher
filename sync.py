import os

from files import download_files


def sync(config):
    output_dir = os.path.expanduser(config["output_directory"])
    for course_id in config["courses"]:
        print(f"Syncing {course_id}")
        download_files(course_id, output_dir)
