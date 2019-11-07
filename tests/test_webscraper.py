from nDash import scraper


def test_webscraper_setup_teardown():
    webscraper = scraper.WebScraper()
    webscraper.setup_driver()
    webscraper.driver.get('https://www.google.com')
    assert webscraper.driver.title == 'Google'
    webscraper.teardown_driver()
