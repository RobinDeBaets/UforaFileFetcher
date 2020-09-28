import os
import sys

from uff.brightspace import BrightspaceAPI
from uff.courses import print_courses
from uff.files import download_files
from uff.setup_config import setup
from uff.sync import sync
from uff.utils import get_config


def show_help():
    print("Commands:")
    print("help")
    print("setup")
    print("courses <config>")
    print("download <course_id> <config> <output_dir>")
    print("sync <config>")


def run():
    if len(sys.argv) <= 1:
        show_help()
    else:
        command = sys.argv[1].lower()
        if command == "courses":
            config = get_config(sys.argv[2])
            brightspace_api = BrightspaceAPI.from_config(config)
            print_courses(brightspace_api)
        elif command == "setup":
            setup()
        elif command == "download":
            course_id = None
            try:
                course_id = int(sys.argv[2])
            except ValueError:
                print("Invalid course id")
                exit()
            config = get_config(sys.argv[3])
            brightspace_api = BrightspaceAPI.from_config(config)
            if 5 <= len(sys.argv):
                output_dir = os.path.expanduser(sys.argv[4])
            else:
                output_dir = os.getcwd()
            download_files(brightspace_api, course_id, output_dir)
        elif command == "sync":
            config = get_config(sys.argv[2])
            sync(config)
        else:
            show_help()


if __name__ == "__main__":
    run()
