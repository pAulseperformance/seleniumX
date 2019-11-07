from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import logging


class WebScraper:
    def __init__(self):
        self.driver = None
        self.logger = logging.getLogger(__name__)
        self.logger.debug('creating an instance of %s', __class__)


    def setup_driver(self, driver='Firefox', options=None):
        self.logger.info('Setting up webriver with %s', driver)
        if driver == 'Firefox':
            opts = webdriver.firefox.options.Options()
            opts.headless = True
            self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=opts)
        elif driver == 'Chrome':
            opts = webdriver.chrome.options.Options()
            opts.headless = True
            self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=opts)
        else:
            self.logger.error('Driver Not supported.')

    def teardown_driver(self):
        self.driver.quit()
