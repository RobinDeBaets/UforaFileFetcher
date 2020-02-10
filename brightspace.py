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


class BrightspaceAPI(metaclass=Singleton):

    def __init__(self):
        self._session = None

    def get_session(self):
        if not self._session:
            # Lazy load the session
            import utils
            credentials = utils.get_credentials()
            self._session = get_session(credentials["username"], credentials["password"])
        return self._session
