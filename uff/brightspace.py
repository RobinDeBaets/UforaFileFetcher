import traceback

from uff.ufora_login import get_session

ufora = "https://ufora.ugent.be"
root = f"{ufora}/d2l/api"
lp_root = f"{root}/lp/1.25"
le_root = f"{root}/le/1.40"


class APIError(Exception):
    pass


class BrightspaceAPI:

    def __init__(self, email, password, otc_secret):
        self._session = None
        self.email = email
        self.password = password
        self.otc_secret = otc_secret
        try:
            self.session = get_session(self.email, self.password, self.otc_secret)
        except Exception:
            print(traceback.format_exc())
            raise APIError("No session could be created. Please make sure your credentials are correct")

    @staticmethod
    def from_config(config):
        credentials = config["credentials"]
        return BrightspaceAPI(credentials["email"], credentials["password"], credentials["otc_secret"])
