from uff.ufora_login import get_session
from uff.utils import get_config

ufora = "https://ufora.ugent.be"
root = f"{ufora}/d2l/api"
lp_root = f"{root}/lp/1.25"
le_root = f"{root}/le/1.40"


class BrightspaceAPI:

    def __init__(self, username, password):
        self._session = None
        self.username = username
        self.password = password

    def get_session(self):
        if not self._session:
            self._session = get_session(self.username, self.password)
        return self._session

    @staticmethod
    def from_config(config):
        credentials = config["credentials"]
        return BrightspaceAPI(credentials["username"], credentials["password"])
