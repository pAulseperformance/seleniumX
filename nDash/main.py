from scraper import WebScraper
import logging


logging.basicConfig(format="%(asctime)s %(levelname)s:%(name)s: %(message)s", datefmt='%H:%M:%S',
                        level=logging.DEBUG, )
logging.getLogger(__name__)


ws = WebScraper()
ws.setup_driver()
ws.driver.get('https://ipleak.net/')
