import json
import os
import re
import string
from json import JSONDecodeError
from os import path

from tqdm import tqdm

from brightspace import BrightspaceAPI

filename_whitelist = " +:_ë-.'" + string.ascii_letters + string.digits
brightspace_api = BrightspaceAPI()
dir_path = os.path.dirname(os.path.realpath(__file__))


def clean_filename(name):
    return "".join([c for c in name if c in filename_whitelist])


# Some courses have an annoying prefix, we'll ignore it
course_prefix = re.compile("^[^-]+ - ")


def create_filepath(course, path):
    course_name = course["OrgUnit"]["Name"]
    course_name = course_prefix.sub("", course_name)
    return "/".join(
        [clean_filename(course_name)] + [clean_filename(module["Title"]) for module in path])


def create_filename(item):
    extension = item["Url"].split(".")[-1]
    extension = extension.split("?")[0]
    return clean_filename(item["Title"]) + "." + extension


def create_filename_without_extension(item):
    return clean_filename(item["Title"])


def download_from_url(url, filepath):
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
        pbar.close()


def get_credentials():
    try:
        with open(f"{dir_path}/credentials.json", "r") as f:
            credentials = json.loads(f.read())
            for key in ["username", "password"]:
                if key not in credentials:
                    print(f"{key} missing from credentials")
                    exit()
            return credentials
    except FileNotFoundError:
        print("File credentials.json does not exist")
    except JSONDecodeError:
        print("File credentials.json is not a valid json file")
    exit()


def get_config():
    try:
        with open(f"{dir_path}/config.json", "r") as f:
            config = json.loads(f.read())
            for key in ["output_directory", "courses"]:
                if key not in config:
                    print(f"{key} missing from config")
                    exit()
            try:
                config["courses"] = list(map(int, config["courses"]))
            except ValueError:
                print("File config.json contains invalid course id")
                exit()
            return config
    except FileNotFoundError:
        print("File config.json does not exist")
    except JSONDecodeError:
        print("File config.json is not a valid json file")
    exit()


def write_to_config(key, value):
    try:
        with open(f"{dir_path}/config.json", "r+") as jsonFile:
            data = json.load(jsonFile)

            tmp = data[key]
            data[key] = value

            jsonFile.seek(0)  # rewind
            json.dump(data, jsonFile)
            jsonFile.truncate()

    except FileNotFoundError:
        print("File config.json does not exist")
    except JSONDecodeError:
        print("File config.json is not a valid json file")
    exit()
