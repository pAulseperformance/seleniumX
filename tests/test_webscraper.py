from nDash import scraper


def test_webscraper_setup_teardown():
    webscraper = scraper.WebScraper()
    webscraper.setup_driver()
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

def test_scroll_into_view():
    url = 'https://ipleak.net/'
    webscraper = scraper.WebScraper()
    webscraper.setup_driver()
    webscraper.driver.get(url)
    # time.sleep(5)
    element_cn = 'center_box'
    element = webscraper.driver.find_element_by_class_name(element_cn)
    webscraper.js_scroll_into_view(element=element)

def test_login_and_authenticate():
    # Login to ndash
    pass
