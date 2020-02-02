#!/usr/bin/env python3
import sys

from courses import print_courses
from files import get_files
from setup import setup


def show_help():
    print("Commands:")
    print("help")
    print("setup")
    print("courses")


def fetch():
    print("fetching...")


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        show_help()
    else:
        command = sys.argv[1].lower()
        if command == "courses":
            print_courses()
        elif command == "setup":
            setup()
        elif command == "files":
            get_files(52413)
        else:
            show_help()
