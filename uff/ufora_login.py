import os

import pyotp
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

LOGIN_URL = "https://elosp.ugent.be/welcome"

NEXT_BUTTON = "//input[@type='submit' and @value='Next']"
SIGN_IN_BUTTON = "//input[@type='submit' and @value='Sign in']"
PASSWORD_BUTTON = "//input[@name='passwd']"
OTC_BUTTON = "//input[@name='otc']"
VERIFY_BUTTON = "//input[@type='submit' and @value='Verify']"

def get_session(username, password, otc_secret):
    print("Launching headless browser to login")
    os.environ["WDM_LOG_LEVEL"] = "0"
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.get(LOGIN_URL)
    driver.find_element_by_id("ugent-login-button").click()
    driver.find_element_by_id("username").send_keys(username)
    driver.find_element_by_id("wp-submit").click()
    driver.find_element_by_xpath("//a[contains(@title,'Sign In')]").click()
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, NEXT_BUTTON))
    ).click()

    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, PASSWORD_BUTTON))).send_keys(password)

    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, SIGN_IN_BUTTON))
    ).click()

    otc_button = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, OTC_BUTTON))
    )
    totp = pyotp.TOTP(otc_secret)
    code = totp.now()

    otc_button.send_keys(code)

    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, VERIFY_BUTTON))
    ).click()


    WebDriverWait(driver, 20).until(
        EC.title_is("Startpagina - ufora")
    )
    cookies = driver.get_cookies()
    session = requests.Session()
    for cookie in cookies:
        session.cookies.set(cookie["name"], cookie["value"])
    return session
