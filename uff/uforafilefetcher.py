import os
import sys
from concurrent.futures.thread import ThreadPoolExecutor

from uff.brightspace import BrightspaceAPI, APIError
from uff.courses import print_courses
from uff.files import download_files
from uff.setup_config import setup
from uff.sync import sync, DOWNLOAD_THREADS
from uff.utils import get_config


def show_help(commands):
    print("Possible commands are:")
    for command in commands:
        print(f"\t{command} {' '.join(commands[command])}")


def check_command_valid(args, commands):
    if len(args) <= 1:
        print("A command should be given")
        show_help(commands)
        exit(1)
    command = args[1].lower()
    if command not in commands:
        print("Command unknown")
        show_help(commands)
        exit(1)
    required_args_count = len([arg for arg in commands[command] if arg.startswith("<")])
    if command not in commands:
        print("Command unknown")
        show_help(commands)
        exit(1)
    elif (len(args) - 2) < required_args_count:
        # Ignore first two arguments, which are the executable and the command
        print(f"The command {command} needs at least {required_args_count} arguments: {', '.join(commands[command])}")
        exit(1)


def run():
    commands = {
        "help": [],
        "setup": [],
        "courses": ["<config>"],
        "download": ["<course_id>", "<config>", "[output_dir]"],
        "sync": ["<config>"]
    }
    args = sys.argv
    check_command_valid(args, commands)
    command = args[1].lower()
    if command == "courses":
        config = get_config(args[2])
        brightspace_api = BrightspaceAPI.from_config(config)
        print_courses(brightspace_api)
    elif command == "setup":
        setup()
    elif command == "download":
        course_id = None
        try:
            course_id = int(args[2])
        except ValueError:
            print("Invalid course id")
            exit()
        config = get_config(args[3])
        brightspace_api = BrightspaceAPI.from_config(config)
        if 5 <= len(args):
            output_dir = os.path.expanduser(args[4])
        else:
            output_dir = os.getcwd()
        with ThreadPoolExecutor(max_workers=DOWNLOAD_THREADS) as download_pool:
            download_files(brightspace_api, course_id, output_dir, download_pool)
    elif command == "sync":
        config = get_config(args[2])
        sync(config)
    else:
        show_help(commands)


if __name__ == "__main__":
    try:
        run()
    except APIError as e:
        print(e)
        exit(1)
