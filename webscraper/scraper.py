import random
import time
from webscraper.randomizer import get_bspline

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import logging


logging.basicConfig(format="%(asctime)s %(levelname)s:%(name)s: %(message)s", datefmt='%H:%M:%S',
                        level=logging.INFO, )
logging.getLogger(__name__)


class WebScraper:
    def __init__(self):
        self.driver = None
        self.logger = logging.getLogger(__name__)
        self.logger.debug('creating an instance of %s', __class__)
        self.implicit_wait_range = (0, 0)
        self.implicit_wait_time = self.randomize_wait_time()
        self.logger.info(f"Implicit Wait time is set to {self.implicit_wait_time}")
        self.sleep_range = (2, 10)  # Should probably make this range to 5 minutes for each page to imitate human behavior

    def setup_driver(self, driver: object = 'Chrome') -> object:
        self.logger.info('Setting up webdriver with %s', driver)
        if driver == 'Firefox':
            options = webdriver.FirefoxOptions()
            options.headless = False
            self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)
        elif driver == 'Chrome':
            options = webdriver.ChromeOptions()
            # Experimental Options used to undefine navigator.webdriver = true
            # Only tested in chrome. Does not work in headless mode.
            # These options avoid bot detection from distil.
            # More info here: https://stackoverflow.com/questions/53039551/selenium-webdriver-modifying-navigator-webdriver-flag-to-prevent-selenium-detec?noredirect=1&lq=1
            options.add_argument("start-maximized")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.headless = False
            self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
            self.logger.info("Chromedriver Online.")
        else:
            self.logger.error('Driver Not supported.')
            return

        self.logger.debug(f"Setting Driver Implicit wait time to: {self.implicit_wait_time}")
        self.driver.implicitly_wait(self.implicit_wait_time)

    def randomize_wait_time(self):
        return random.uniform(*self.implicit_wait_range)

    def random_sleep(self, sleep_range=None):
        if sleep_range is None:
            time.sleep(random.uniform(*self.sleep_range))
        else:
            time.sleep(random.uniform(*sleep_range))

    def teardown_driver(self):
        self.driver.quit()
        self.logger.info('Driver Offline')

    def check_safe_scraping(self):
        # This function should check if the webpage to be scraped has bot detection.
        # Open up chrome tools and search for distil files or js.
        # driver.get("https://www.controller.com")
        # Navigate across this domain and don't get blocked.
        pass

    def check_safe_headless(self):
        # This function checks if the headless browser is being deteced as a headless browser.
        # Currenly it will fail the test everytime we run headless, there might be a workaround for this
        # For now we run the browser with a graphical interface to avoid detection.
        url = 'https://ipleak.net/'
        xpath = '/html/body/div/div[3]/div[10]/div[1]/table/tbody/tr[1]/td[2]'
        text = 'Chrome'
        self.driver.get(url)
        try:
            WebDriverWait(self.driver, 20).until(EC.text_to_be_present_in_element((By.XPATH, xpath), text))
            self.logger.info('Page Loaded.')
        except Exception as e:
            self.logger.error(e)

        if self.driver.page_source.find('HeadlessChrome') > 0:
            self.logger.info('Your browser is currently being detected as headless, '
                             'reconfigure your options or run headless=False')
        else:
            self.logger.info('Your headless browser has not been detected. :)')

    def explicit_wait(self, element_name, time=10):
        # TODO  Impliment this
        selector = By.ID
        try:
            element = WebDriverWait(self.driver, time).until(EC.presence_of_element_located((selector, element_name)))
            return element
        except Exception as e:
            self.logger.error(e)

    def save_screenshot(self):
        title = self.driver.title.split(' ')
        if len(title) > 2:
            title = ''.join(self.driver.title.split(' ')[:2])
        self.driver.save_screenshot(f'{title}.png')
        self.logger.info(f"Saved Screenshot to {title}.png")

    def _js_inject_js(self, js=None, is_async=True, *args):
        if is_async:
            self.driver.execute_async_script(js, *args)
        else:
            self.driver.execute_script(js, *args)

    def js_scroll_into_view(self, element):
        # Uses Javascript to scroll an element into view.
        self.logger.debug("Scrolling element into view")
        js = "arguments[0].scrollIntoView();"
        try:
            # self.driver.execute_script("arguments[0].scrollIntoView();", element)
            self._js_inject_js(js, False, element)
        except Exception as e:
            self.logger.error('Element not found?\n %s', e)
            raise e

    def js_scroll_to_bottom(self):
        # Scrolls to bottom of page. Good for inifinite feeds like FB or twitter.
        self.logger.debug("Scrolling window to bottom...")
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def js_webdriver_false(self):
        # Excecute this script on every page load before other client side java runs.
        # Not possible with just selenium.
        # Read more here https://intoli.com/blog/javascript-injection/
        # injected_javascript = "Object.defineProperty(navigator, 'webdriver',{ get: () => false, });"
        pass

    def get_all_unique_links(self):
        # Finds all links on current page and returns a set of unique links
        elems = self.driver.find_elements_by_xpath("//a[@href]")
        links = []
        for elem in elems:
            links.append(elem.get_attribute("href"))
        self.logger.info(f"{len(set(links))} unique links collected from {self.driver.title}")
        return set(links)

    def random_move_mouse(self):
        # Imitate human mouse movements with bspline movements.

        action = ActionChains(self.driver)

        startElement = self.driver.find_element_by_id("//a[href]")

        # First, go to your start point or Element
        action.move_to_element_with_offset(startElement, 0, 0)
        action.perform()

        for mouse_x, mouse_y in get_bspline():
            action.move_by_offset(mouse_x, mouse_y)
            action.perform()
            self.random_sleep(sleep_range=(0, .05))
            print(mouse_x, mouse_y)

    def test_distil_bot_detection(self):
        # url = 'https://www.controller.com'
        # ws = WebScraper()
        # ws.setup_driver()
        # ws.driver.get(url)
        #
        # links = self.get_all_links()
        # self.sleep_random()
        # ws.driver.get(links[10])
        pass

    def test_google(self):
        self.setup_driver()
        self.driver.get('https://www.google.com')
        search_element = self.driver.find_element_by_name('q')
        self.random_send_keys('cats', search_element)
        search_element.submit()

    def random_send_keys(self, keys, element):
        for key in keys:
            element.send_keys(key)
            self.random_sleep(sleep_range=(0, 1))

    def random_navigate_element_to_element(self):
        # TODO
        # Get starting element Coordinates
        # Get ending element coordinates
        # Randomize mouse path to end element
        # element.location_once_scrolled_into_view
        pass
