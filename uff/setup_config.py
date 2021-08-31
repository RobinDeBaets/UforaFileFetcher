import json

import inquirer
from inquirer import Path

from uff.brightspace import BrightspaceAPI
from uff.courses import get_courses_list
from uff.ufora_login import get_session


def setup():
    username = inquirer.text(message="What's your username")
    password = inquirer.password(message="What's your password")
    otc_secret = inquirer.password(message="What's your 2FA secret?")
    session = get_session(username, password, otc_secret)
    if session is None:
        print("Invalid login credentials")
        return
    config_file = inquirer.shortcuts.path(message="Specify config file", path_type=Path.FILE)
    output_directory = inquirer.shortcuts.path(message="Specify output directory", path_type=Path.DIRECTORY)
    brightspace_api = BrightspaceAPI(username, password, otc_secret)
    courses = get_courses_list(brightspace_api)
    selected_courses = inquirer.checkbox(message="Select courses to sync (press enter when ready)",
                                         choices=courses
                                         )
    course_ids = [courses[course] for course in selected_courses]
    with open(config_file, "w+") as f:
        f.write(json.dumps({
            "output_directory": output_directory,
            "courses": course_ids,
            "credentials": {
                "username": username,
                "password": password,
                "otc_secret": otc_secret
            }
        }, indent=4))
    print("Setup complete!")
