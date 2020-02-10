import os
from os import path

import pdfkit as pdfkit

from brightspace import BrightspaceAPI, le_root, ufora
from courses import get_course
from utils import create_filename, create_filepath, download_from_url, create_filename_without_extension

brightspace_api = BrightspaceAPI()

options = {"quiet": ""}


def get_module(module_id, course_id):
    return brightspace_api.get_session().get(f"{le_root}/{course_id}/content/modules/{module_id}/structure/").json()


def download_files(course_id, output_dir):
    course = get_course(course_id)
    if course is None:
        return
    modules = brightspace_api.get_session().get(f"{le_root}/{course_id}/content/root/").json()
    for module in modules:
        traverse_element(module, course_id, [], course, output_dir)


def create_metadata(filepath, description, title):
    if not path.exists(filepath):
        # Only create metadata if it doesn't exist
        os.makedirs("/".join(filepath.split("/")[:-1]), exist_ok=True)
        print("Creating metadata " + filepath.split("/")[-1])
        pdfkit.from_string(f"<base href={ufora}><style>body{{background:white}}</style><h1>{title}</h1>{description}",
                           filepath,
                           options=options)


def download_file(item, path, course, output_dir):
    filepath = create_filepath(course, path)
    description = item["Description"]["Html"]
    topic_type = item["TopicType"]
    title = item["Title"]
    if topic_type == 1:
        filename = create_filename(item)
        full_path = f"{output_dir}/{filepath}/{filename}"
        # These documents are real files that we want to download
        download_from_url(f"""{ufora}{item["Url"]}""", full_path)
        if item["Url"].endswith(".html"):
            # HTML files on Ufora need a little special treatment
            # We'll prepend a title, <base> tag and convert them to pdf
            with open(full_path, "r") as f:
                content = f.read()
            filename_without_extension = ".".join(filename.split(".")[:-1])
            description_path = f"{output_dir}/{filepath}/{filename_without_extension}.pdf"
            create_metadata(description_path, content, filename_without_extension)
            new_content = f"<base href={ufora}><h1>{title}</h1>{content}"
            with open(full_path, "w") as f:
                f.write(new_content)
        elif description:
            # Choosing this filename might cause an overlap...
            filename_without_extension = ".".join(filename.split(".")[:-1])
            description_path = f"{output_dir}/{filepath}/{filename_without_extension}.pdf"
            create_metadata(description_path, description, filename_without_extension)
    elif topic_type == 3:
        # These documents are just clickable links, we'll render them in a pdf
        url = item["Url"]
        filename = create_filename_without_extension(item)
        full_path = f"{output_dir}/{filepath}/{filename}"
        create_metadata(f"{full_path}.pdf", f"<a href={url}>{url}</a>{description}", item["Title"])
    else:
        print(f"Don't know this topic type: {topic_type}")
        exit()


def download_module(item, path, course, output_dir):
    description = item["Description"]["Html"]
    if description:
        filepath = create_filepath(course, path)
        description_path = f"{output_dir}/{filepath}/metadata.pdf"
        create_metadata(description_path, description, filepath.split("/")[-1])


def traverse_element(item, course_id, path, course, output_dir):
    if item["Type"] == 1:
        download_file(item, path, course, output_dir)
    else:
        path.append(item)
        download_module(item, path, course, output_dir)
        for sub_element in get_module(item["Id"], course_id):
            traverse_element(sub_element, course_id, path, course, output_dir)
        path.pop()
