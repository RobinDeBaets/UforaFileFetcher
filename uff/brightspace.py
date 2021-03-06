from uff.ufora_login import get_session

ufora = "https://ufora.ugent.be"
root = f"{ufora}/d2l/api"
lp_root = f"{root}/lp/1.25"
le_root = f"{root}/le/1.40"


class APIError(Exception):
    pass


class BrightspaceAPI:

    def __init__(self, username, password):
        self._session = None
        self.username = username
        self.password = password
        self.session = get_session(self.username, self.password)
        if self.session is None:
            raise APIError("No session could be created. Please make sure your credentials are correct")

    @staticmethod
    def from_config(config):
        credentials = config["credentials"]
        return BrightspaceAPI(credentials["username"], credentials["password"])
