import argparse
import getopt
import json
import string
import sys

from ufora_login import get_cookies


def setup():
    parser = argparse.ArgumentParser()
    parser.add_argument("setup")
    parser.add_argument("--username")
    parser.add_argument("--password")
    args = parser.parse_args()
    username = args.username
    password = args.password
    if not username:
        username = input("Ufora username: ")
    if not password:
        password = input("Ufora password: ")
    cookies = get_cookies(username, password)
    if cookies is None:
        print("Invalid login credentials")
        return
    with open("credentials.json", "w+") as f:
        f.write(json.dumps({
            "username": username,
            "password": password
        }))
    print("Setup complete!")
