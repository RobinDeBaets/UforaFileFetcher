import os
from os import path

import pdfkit as pdfkit

from brightspace import BrightspaceAPI, le_root, ufora
from courses import get_course
from utils import create_filename, create_filepath, download_from_url

brightspace_api = BrightspaceAPI()

options = {"quiet": ""}


def get_module(module_id, course_id):
    return brightspace_api.session.get(f"{le_root}/{course_id}/content/modules/{module_id}/structure/").json()


def get_files(course_id):
    course = get_course(course_id)
    modules = brightspace_api.session.get(f"{le_root}/{course_id}/content/root/").json()
    for module in modules:
        traverse_element(module, course_id, [], course)


def create_metadata(filepath, description, title):
    if not path.exists(filepath):
        # Only create metadata if it doesn't exist
        os.makedirs("/".join(filepath.split("/")[:-1]), exist_ok=True)
        print("Creating metadata " + filepath.split("/")[-1])
        pdfkit.from_string(f"<base href={ufora}><style>body{{background:white}}</style><h1>{title}</h1>{description}",
                           filepath,
                           options=options)


def download_file(item, path, course):
    filepath = create_filepath(course, path)
    filename = create_filename(item)
    full_path = f"{filepath}/{filename}"
    description = item["Description"]["Html"]
    topic_type = item["TopicType"]
    if topic_type == 1:
        # These documents are real files that we want to download
        if description:
            description_path = f"{full_path}.metadata.pdf"
            create_metadata(description_path, description, ".".join(filename.split(".")[:-1]))
        download_from_url(f"""{ufora}{item["Url"]}""", full_path)
    elif topic_type == 3:
        # These documents are just clickable links, we'll render them in a pdf
        url = item["Url"]
        create_metadata(f"{full_path}.pdf", f"<a href={url}>{url}</a>{description}", ".".join(filename.split(".")[:-1]))
    else:
        print(f"Don't know this topic type: {topic_type}")
        exit()


def download_module(item, path, course):
    description = item["Description"]["Html"]
    if description:
        filepath = create_filepath(course, path)
        description_path = f"{filepath}/metadata.pdf"
        create_metadata(description_path, description, filepath.split("/")[-1])


def traverse_element(item, course_id, path, course):
    if item["Type"] == 1:
        download_file(item, path, course)
    else:
        path.append(item)
        download_module(item, path, course)
        for sub_element in get_module(item["Id"], course_id):
            traverse_element(sub_element, course_id, path, course)
        path.pop()
