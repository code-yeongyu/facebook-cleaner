from os import environ
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
    print("Filled username")
    password_field.send_keys(password)
    print("Filled password")
    login_button.click()
    print("Clicked Login Button")
    sleep(1)
    print("Logged In")


def open_my_profile():
    driver.get("https://www.facebook.com/me")
    sleep(2)
    print("Opened facebook")


def set_filter_only_friends():
    open_filter_js = """document.querySelector('[aria-label="필터"]').click()"""
    open_combobox_js = """document.querySelectorAll('[role="combobox"]')[3].click()"""
    only_friends_option_js = """document.querySelectorAll('[role="option"]')[1].click()"""
    click_done_js = """document.querySelector('[aria-label="완료"]').click()"""
    sleep(0.5)
    driver.execute_script(open_filter_js)
    print("opened filter popup")
    sleep(0.5)
    driver.execute_script(open_combobox_js)
    print("opened combobox")
    sleep(0.5)
    driver.execute_script(only_friends_option_js)
    print("setted option as public")
    sleep(0.5)
    driver.execute_script(click_done_js)
    print("options have setted")


def set_filter_public():
    open_filter_js = """document.querySelector('[aria-label="필터"]').click()"""
    open_combobox_js = """document.querySelectorAll('[role="combobox"]')[3].click()"""
    public_option_js = """document.querySelectorAll('[role="option"]')[0].click()"""
    click_done_js = """document.querySelector('[aria-label="완료"]').click()"""
    sleep(0.5)
    driver.execute_script(open_filter_js)
    print("opened filter popup")
    sleep(0.5)
    driver.execute_script(open_combobox_js)
    print("opened combobox")
    sleep(0.5)
    driver.execute_script(public_option_js)
    print("setted option as public")
    sleep(0.5)
    driver.execute_script(click_done_js)
    print("options have setted")


def get_article_length() -> int:
    js = """return document.querySelector('[data-pagelet="ProfileTimeline"]').querySelectorAll('[role="article"]').length"""
    return driver.execute_script(js)


def is_article_public(i: int) -> bool:
    js = f"""return document.querySelector('[data-pagelet="ProfileTimeline"]').querySelectorAll('[role="article"]')[{i}].querySelector('img').getAttribute("alt")"""
    proper_text = driver.execute_script(js)
    scopes = ["전체 공개", "친구만", "제외할 친구...", "친구의 친구", "특정 친구", "사용자 지정"]
    return proper_text in ''.join(scopes)


def open_privacy_settings(i: int):
    js = f"""return document.querySelector('[data-pagelet="ProfileTimeline"]').children[{i}].querySelector('img').click()"""
    driver.execute_script(js)
    print(f"opened privacy settings for {i}")
    sleep(0.5)


def set_only_me():
    js = """document.querySelector('[role="dialog"]').children[0].querySelector("div:nth-child(6) > div").click()"""
    driver.execute_script(js)
    print("setted only me")
    sleep(0.5)


def scroll_bottom():
    js = """window.scrollTo(0,0);window.scrollTo(0,document.body.scrollHeight);"""
    driver.execute_script(js)
    print("scrolled to bottom")
    sleep(0.5)


def set_only_me_if_public(i: int):
    error_count = 0
    while True:
        try:
            if is_article_public(i):
                open_privacy_settings(i)
                set_only_me()
            else:
                print(
                    f"skipped {i} because it's already private or not privatable"
                )
            return
        except Exception as e:
            print(e)
            error_count += 1
            if error_count > 3:  # skip if error occured more than 5 times in a same index
                return


username = environ["username"]
password = environ["password"]

login(username, password)
open_my_profile()

last_index = 0
set_filter_only_friends()
while True:
    for i in range(0, 20):
        scroll_bottom()
    article_length = get_article_length()
    print(f"{last_index}/{article_length}")
    for i in range(last_index, article_length):
        set_only_me_if_public(i)
        last_index = i
    if last_index == article_length:
        break
driver.quit()

print("All articles have are now private.")
