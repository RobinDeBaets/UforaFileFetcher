import requests
from bs4 import BeautifulSoup

login_url = "https://ufora.ugent.be/d2l/lp/auth/saml/login"
login_root = "https://login.ugent.be"
d2l_auth_url = "https://ufora.ugent.be/d2l/lp/auth/login/samlLogin.d2l"
password_url = "https://wachtwoord.ugent.be/"


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
        # 90 days to change password (?)
        password_element = saml_html.find("a", {"href": password_url})
        if password_element is None:
            return None
        password_elements = saml_html.find_all("a")
        print(
            f"Warning: please consider updating your password, it will be automatically expire in less than 60 days. Visit {password_elements[1]['href']} to change your password.")
        auth_response = session.get(password_elements[2]["href"])
        saml_html = BeautifulSoup(auth_response.text, "html.parser")
        saml_response_element = saml_html.find("input", {"name": "SAMLResponse"})
    saml_response = saml_response_element["value"]
    session.post(d2l_auth_url, allow_redirects=False, data={
        "SAMLResponse": saml_response
    })
    return session
