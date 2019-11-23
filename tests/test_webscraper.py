from webscraper import scraper
import tempfile
import pytest

@pytest.fixture
def tempd():
    with tempfile.TemporaryDirectory() as td:
        return td


def test_webscraper_setup_teardown(tempd):
    webscraper = scraper.WebScraper()
    webscraper.setup_driver(chrome_driver_path=tempd)
    webscraper.driver.get('https://www.google.com')
    assert webscraper.driver.title == 'Google'
    webscraper.teardown_driver()

# def test_bot_detection():
#     # Distil is a bot detection
#     # Navigate to a known website with bot detector and check if bot can be detected
#     webscraper = scraper.WebScraper()
#     webscraper.setup_driver()
#     webscraper.driver.get('https://www.controller.com')
#     # chase.com


def test_scroll_into_view(tempd):
    url = 'https://ipleak.net/'
    webscraper = scraper.WebScraper()
    webscraper.setup_driver(chrome_driver_path=tempd)
    webscraper.driver.get(url)
    element_cn = 'center_box'
    element = webscraper.driver.find_element_by_class_name(element_cn)
    webscraper.js_scroll_into_view(element=element)


def test_login_and_authenticate():
    # Login to ndash
    pass
