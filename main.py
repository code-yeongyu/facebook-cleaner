import pdb
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

option = Options()

option.add_argument("--disable-infobars")
option.add_argument("--start-maximized")
option.add_argument("--disable-extensions")
option.add_argument("--disable-gpu")
option.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
)
option.add_argument("--test-type")
option.add_argument("--no-first-run")
option.add_argument("--no-default-browser-check")
option.add_argument("--ignore-certificate-errors")
option.add_experimental_option(
    "prefs", {
        "profile.default_content_setting_values.notifications": 1,
        'intl.accept_languages': 'ko-KR',
    })

# open facebook
driver = webdriver.Chrome("chromedriver", options=option)


def login(email: str, password: str):
    driver.get("https://www.facebook.com/")
    email_field = driver.find_element_by_id("email")
    password_field = driver.find_element_by_id("pass")
    login_button = driver.find_element_by_name("login")
    email_field.send_keys(email)
    password_field.send_keys(password)
    login_button.click()
    sleep(1)

