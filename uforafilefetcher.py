#!/usr/bin/env python3
from __future__ import print_function, unicode_literals
from whaaaaat import prompt, print_json

import os
import sys

from courses import print_courses, get_courses_list
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
            course_ids = get_course_choices()
            if 3 <= len(sys.argv):
                output_dir = os.path.expanduser(sys.argv[2])
            else:
                output_dir = os.getcwd()
            for course_id in course_ids:
                download_files(course_id, output_dir)
        elif command == "sync":
            config = get_config()
            sync(config)
        else:
            show_help()


def get_course_choices():
    course_ids = []
    courselist = get_courses_list()
    print(courselist.keys())
    choices = []
    for course in courselist.keys():
        choices.append({'name': course})
    questions = [
        {
            'type': 'checkbox',
            'name': 'courses',
            'message': 'Select courses to download',
            'choices': choices,
            'validate': lambda answer: 'You must choose at least one topping.' \
                if len(answer) == 0 else True
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
