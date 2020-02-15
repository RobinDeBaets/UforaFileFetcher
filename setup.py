import argparse
import getpass
import json

from ufora_login import get_session


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
        password = getpass.getpass(prompt="Ufora password: ")
    session = get_session(username, password)
    if session is None:
        print("Invalid login credentials")
        return
    with open("credentials.json", "w+") as f:
        f.write(json.dumps({
            "username": username,
            "password": password
        }))
    print("Setup complete!")
