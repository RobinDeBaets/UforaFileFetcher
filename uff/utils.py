import json
import os
import re
import string
from json import JSONDecodeError
from os import path
from pathvalidate import sanitize_filename

from tqdm import tqdm

# Some courses have an annoying prefix, we'll ignore it
course_prefix = re.compile("^[^-]+ - ")


def create_filepath(course, path):
    course_name = course["OrgUnit"]["Name"]
    course_name = course_prefix.sub("", course_name)
    return "/".join(
        [sanitize_filename(course_name)] + [sanitize_filename(module["Title"]) for module in path])


def create_filename(item):
    extension = item["Url"].split(".")[-1]
    extension = extension.split("?")[0]
    return sanitize_filename(item["Title"]) + "." + extension


def create_filename_without_extension(item):
    return sanitize_filename(item["Title"])


def download_from_url(brightspace_api, url, filepath):
    if not path.exists(filepath):
        # Only download file if it doesn't exist
        os.makedirs("/".join(filepath.split("/")[:-1]), exist_ok=True)
        file_size = int(brightspace_api.get_session().head(url).headers["Content-Length"])
        pbar = tqdm(
            total=file_size, initial=0,
            unit="B", unit_scale=True, desc="Downloading " + url.split("/")[-1])
        req = brightspace_api.get_session().get(url, stream=True)
        with(open(filepath, "ab")) as f:
            for chunk in req.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    pbar.update(1024)
        pbar.update(file_size)
        pbar.close()


def get_config(config_file):
    try:
        with open(config_file, "r") as f:
            return json.loads(f.read())
    except FileNotFoundError:
        print(f"File {config_file} does not exist")
    except JSONDecodeError:
        print(f"File {config_file} is not a valid json file")
    exit()

