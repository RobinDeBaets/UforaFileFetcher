import os
import threading

from uff import pdf_wrapper
from uff.brightspace import le_root, ufora
from uff.courses import get_course
from uff.ppt_converter import convert_to_pdf
from uff.utils import create_filename, create_filepath, download_from_url, create_filename_without_extension


def get_module(brightspace_api, module_id, course_id):
    return brightspace_api.session.get(f"{le_root}/{course_id}/content/modules/{module_id}/structure/").json()


def download_files(brightspace_api, course_id, output_dir, download_pool):
    course = get_course(brightspace_api, course_id)
    if course is None:
        print(f"Could not find course {course_id}")
        exit()
    modules = brightspace_api.session.get(f"{le_root}/{course_id}/content/root/").json()
    threads = []
    for module in modules:
        thread = threading.Thread(target=traverse_element,
                                  args=(brightspace_api, module, course_id, [], course, output_dir, download_pool))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()


def create_metadata(filepath, description, title):
    if not os.path.isfile(filepath):
        # Only create metadata if it doesn't exist
        os.makedirs("/".join(filepath.split("/")[:-1]), exist_ok=True)
        print("Creating metadata " + filepath.split("/")[-1])
        pdf_wrapper.from_string(
            f"""<link rel="stylesheet" href="https://unpkg.com/sakura.css/css/sakura.css" type="text/css"><base href={ufora}><style>body{{background:white}}</style><h1>{title}</h1>{description}""",
            filepath)


def download_file(brightspace_api, item, path, course, output_dir):
    filepath = create_filepath(course, path)
    description = item["Description"]["Html"]
    topic_type = item["TopicType"]
    title = item["Title"]
    url = item["Url"]
    if topic_type == 1:
        filename = create_filename(item)
        filename_without_extension = ".".join(filename.split(".")[:-1])
        full_path = f"{output_dir}/{filepath}/{filename}"
        # These documents are regular files that we want to download
        download_from_url(brightspace_api, f"""{ufora}{url}""", full_path)
        if url.endswith(".html"):
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
            description_path = f"{output_dir}/{filepath}/{filename_without_extension}_metadata.pdf"
            create_metadata(description_path, description, filename_without_extension)
        if url.endswith(".pptx") or url.endswith(".ppt"):
            # ppt and pptx files can be converted to PDF if unoconv is present
            new_pdf_path = f"{output_dir}/{filepath}/{filename_without_extension}_converted.pdf"
            if not os.path.isfile(new_pdf_path):
                convert_to_pdf(full_path, new_pdf_path)

    elif topic_type == 3:
        # These documents are just clickable links, we'll render them in a pdf
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


def traverse_element(brightspace_api, item, course_id, path, course, output_dir, download_pool):
    if item["Type"] == 1:
        download_pool.submit(download_file, brightspace_api, item, path, course, output_dir)
    else:
        path.append(item)
        download_module(item, path, course, output_dir)

        threads = []
        for sub_element in get_module(brightspace_api, item["Id"], course_id):
            thread = threading.Thread(target=traverse_element,
                                      args=(brightspace_api, sub_element, course_id, path[:], course, output_dir,
                                            download_pool))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
