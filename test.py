from nDash.scraper import WebScraper
import time
# url = 'https://intoli.com/blog/making-chrome-headless-undetectable/chrome-headless-test.html'

url = 'https://www.google.com'
ws = WebScraper()
ws.setup_driver()
ws.driver.get(url)

