#!/usr/bin/env python3
from __future__ import print_function, unicode_literals
from whaaaaat import prompt

import os
import sys

from courses import print_courses, get_courses_list
from files import download_files
from setup import setup
from sync import sync
from utils import get_config, write_to_config


def show_help():
    print("Commands:")
    print("help")
    print("setup")
    print("courses")
    print("download <course_id> <output_dir>")
    print("sync")
    print("config")


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
            course_ids = get_course_choices("Select courses to download")
            if 3 <= len(sys.argv):
                output_dir = os.path.expanduser(sys.argv[2])
            else:
                output_dir = os.getcwd()
            for course_id in course_ids:
                download_files(course_id, output_dir)
        elif command == "sync":
            config = get_config()
            sync(config)
        elif command == "config":
            verify = [{
                "type": "rawlist",
                "message": "Select which variables you want to change",
                "name": "verification",
                "choices": [
                    "Download directory", "Selected courses", "Both", "Exit"
                ]
            }]

            answer = prompt(verify)["verification"]

            if answer == "Exit":
                exit()
            if answer == "Download directory" or answer == "Both":
                directory_question = [({
                    "type": "input",
                    "message": "Enter your preferred download directory. Leave empty to reset.",
                    "name": "directory"
                })]

                directory_answer = prompt(directory_question)
                output_directory = directory_answer["directory"]
                if output_directory == "":
                    output_directory = "~/UforaFileFetcher"

                write_to_config("output_directory", output_directory)

            if answer == "Selected courses" or answer == "Both":
                course_ids = get_course_choices("Select courses to add to config")
                write_to_config("courses", course_ids)

            print(answer)

        else:
            show_help()


def get_course_choices(message):
    course_ids = []
    courselist = get_courses_list()
    print(courselist.keys())
    choices = []
    for course in courselist.keys():
        choices.append({"name": course})
    questions = [
        {
            "type": "checkbox",
            "name": "courses",
            "message": message,
            "choices": choices
        }
    ]

    answers = prompt(questions)
    while len(answers["courses"]) < 1:
        print("You must select at least one course")
        print()
        answers = prompt(questions)
    for answer in answers["courses"]:
        course_ids.append(courselist[answer])
    return course_ids


if __name__ == "__main__":
    run()
