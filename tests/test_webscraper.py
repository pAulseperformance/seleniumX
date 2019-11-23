from seleniumX import scraper
import tempfile
import pytest
from selenium.webdriver.common.by import By
import os

@pytest.fixture
def tempd():
    with tempfile.TemporaryDirectory() as td:
        return td


def test_webscraper_setup_teardown(tempd):
    ws = scraper.WebScraper()
    ws.setup_driver(chrome_driver_path=tempd)
    ws.driver.get('https://www.google.com')
    assert ws.driver.title == 'Google'
    ws.teardown_driver()


def test_login_and_authenticate_linkedin(tempd):
    login_url = 'https://www.linkedin.com/login'
    ws = scraper.WebScraper()
    ws.setup_driver(chrome_driver_path=tempd)
    ws.driver.get(login_url)
    user_element = ws.driver.find_element(By.ID, "username")
    pass_element = ws.driver.find_element(By.ID, "password")
    user_name = os.environ.get("LINKEDIN_USERNAME")
    password = os.environ.get("LINKEDIN_PASSWORD")
    login_btn = ws.driver.find_element_by_class_name(
            'login__form_action_container')
    ws.login_and_authenticate(login_btn, user_element, pass_element, user_name, password)



# def test_bot_detection():
#     # Distil is a bot detection
#     # Navigate to a known website with bot detector and check if bot can be detected
#     seleniumX = scraper.WebScraper()
#     seleniumX.setup_driver()
#     seleniumX.driver.get('https://www.controller.com')
#     # chase.com


def test_scroll_into_view(tempd):
    url = 'https://ipleak.net/'
    webscraper = scraper.WebScraper()
    webscraper.setup_driver(chrome_driver_path=tempd)
    webscraper.driver.get(url)
    element_cn = 'center_box'
    element = webscraper.driver.find_element_by_class_name(element_cn)
    webscraper.js_scroll_into_view(element=element)
