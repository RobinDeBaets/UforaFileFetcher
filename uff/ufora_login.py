import requests
from bs4 import BeautifulSoup

login_url = "https://ufora.ugent.be/d2l/lp/auth/saml/login"
login_root = "https://login.ugent.be"
d2l_auth_url = "https://ufora.ugent.be/d2l/lp/auth/login/samlLogin.d2l"


def get_session(username, password):
    session = requests.Session()
    login_response = session.get(login_url)
    login_html = BeautifulSoup(login_response.text, "html.parser")
    csrf_token = login_html.find("input", {"name": "csrfToken"})["value"]
    action_url = login_html.find("form", {"id": "fm1"})["action"]
    auth_response = session.post(f"{login_root}{action_url}", data={
        "username": username,
        "password": password,
        "csrfToken": csrf_token,
        "NEGOTIATE_AUTOLOGIN_ENABLE": "True",
        "wp-submit": "Log+in"
    })
    saml_html = BeautifulSoup(auth_response.text, "html.parser")
    saml_response_element = saml_html.find("input", {"name": "SAMLResponse"})
    if saml_response_element is None:
        return None
    saml_response = saml_response_element["value"]
    session.post(d2l_auth_url, allow_redirects=False, data={
        "SAMLResponse": saml_response
    })
    return session
