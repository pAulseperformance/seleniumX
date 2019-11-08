from nDash.scraper import WebScraper
import time
# url = 'https://intoli.com/blog/making-chrome-headless-undetectable/chrome-headless-test.html'

url = 'https://www.google.com'
url = "https://codepen.io/falldowngoboone/pen/PwzPYv"
ws = WebScraper()
ws.setup_driver()
ws.driver.get(url)

ws.move_mouse_random()