import logging
import os

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

LOGIN_URL = "https://elosp.ugent.be/welcome"


def get_session(username, password):
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
        EC.presence_of_element_located((By.XPATH, "//input[@name='passwd']"))
    )
    driver.find_element_by_xpath("//input[@name='passwd']").send_keys(password)
    driver.find_element_by_xpath("//input[@type='submit']").click()
    driver.find_element_by_xpath("//input[@type='submit']").click()
    cookies = driver.get_cookies()
    session = requests.Session()
    for cookie in cookies:
        session.cookies.set(cookie["name"], cookie["value"])
    return session
