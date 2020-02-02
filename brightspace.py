import json

from ufora_login import get_session

ufora = "https://ufora.ugent.be"
root = f"{ufora}/d2l/api"
lp_root = f"{root}/lp/1.25"
le_root = f"{root}/le/1.40"


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def get_credentials():
    with open("credentials.json", "r") as f:
        return json.loads(f.read())


class BrightspaceAPI(metaclass=Singleton):

    def __init__(self):
        credentials = get_credentials()
        self.session = get_session(credentials["username"], credentials["password"])
