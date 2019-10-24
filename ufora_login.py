import requests
from bs4 import BeautifulSoup

login_url = "https://ufora.ugent.be/d2l/lp/auth/saml/login"
d2l_auth_url = "https://ufora.ugent.be/d2l/lp/auth/login/samlLogin.d2l"


def get_cookies(username, password):
    login_response = requests.get(login_url)
    login_html = BeautifulSoup(login_response.text, "html.parser")
    auth_state = login_html.find("input", {"name": "AuthState"})["value"]
    auth_response = requests.post(login_response.url, data={
        "username": username,
        "password": password,
        "AuthState": auth_state,
        "NEGOTIATE_AUTOLOGIN_ENABLE": "True",
        "wp-submit": "Log+in"
    })
    saml_html = BeautifulSoup(auth_response.text, "html.parser")
    saml_response_element = saml_html.find("input", {"name": "SAMLResponse"})
    if saml_response_element is None:
        return None
    saml_response = saml_response_element["value"]
    session = requests.session()
    brightspace_response = session.post(d2l_auth_url, allow_redirects=False, data={
        "SAMLResponse": saml_response
    })
    return brightspace_response.cookies


print(get_cookies("abc", "def"))
