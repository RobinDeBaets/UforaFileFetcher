#!/usr/bin/env python3
import os
import sys

from courses import print_courses
from files import download_files
from setup import setup
from sync import sync
from utils import get_config


def show_help():
    print("Commands:")
    print("help")
    print("setup")
    print("courses")
    print("download <course_id> <output_dir>")
    print("sync")


def run():
    if len(sys.argv) <= 1:
        show_help()
    else:
        command = sys.argv[1].lower()
        if command == "courses":
            print_courses()
        elif command == "setup":
            setup()
        elif command == "download":
            course_id = None
            try:
                course_id = int(sys.argv[2])
            except ValueError:
                print("Invalid course id")
                exit()
            if 4 <= len(sys.argv):
                output_dir = os.path.expanduser(sys.argv[3])
            else:
                output_dir = os.getcwd()
            download_files(course_id, output_dir)
        elif command == "sync":
            config = get_config()
            sync(config)
        else:
            show_help()


if __name__ == "__main__":
    run()
