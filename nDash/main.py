import scraper
import logging


logging.basicConfig(format="%(asctime)s %(levelname)s:%(name)s: %(message)s", datefmt='%H:%M:%S',
                        level=logging.DEBUG, )
logging.getLogger(__name__)


ws = scraper.WebScraper()
ws.logger
ws.setup_driver()
ws.driver.get('https://www.google.com')
