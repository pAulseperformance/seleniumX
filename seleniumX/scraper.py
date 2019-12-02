import random
import time
# from seleniumX.randomizer import get_bspline
from sys import platform
import os
from typing import Tuple, Dict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.events import (
    EventFiringWebDriver,
    AbstractEventListener,
)

from webdriver_manager.chrome import ChromeDriverManager
import logging


PAGE_LOAD_TIMEOUT_IN_SEC = 60
IMPLICITLY_WAIT_RANGE = (0, 0)  # We use a range so the wait times can be randomized.
SCRIPT_TIMEOUT_IN_SEC = 60
VERBOSE = False


class MyListener(AbstractEventListener):
    """ A Wrapper around an arbitrary webdriver instance which support firing events."""

    def before_navigate_to(self, url, driver):
        if VERBOSE:
            print("Before navigate to %s" % url)

    def after_navigate_to(self, url, driver):
        if VERBOSE:
            print("After navigate to %s" % url)
        WebScraper.random_sleep()

    def on_exception(self, exception, driver):
        if VERBOSE:
            self.logger.info("On exception listener", exception)
        WebScraper.random_sleep()

    def before_find(self, by, value, driver):
        if VERBOSE:
            print(f"Before find by {by} with  {value}")

    def after_find(self, by, value, driver):
        if VERBOSE:
            print(f"After find by {by} with  {value}")

    def before_click(self, element, driver):
        if VERBOSE:
            print(f"Before click {element}")

    def after_click(self, element, driver):
        if VERBOSE:
            print(f"After click {element}")

    def before_execute_script(self, script, driver):
        if VERBOSE:
            print(f"Before Execute Script {script}")

    def after_execute_script(self, script, driver):
        if VERBOSE:
            print(f"After Execute Script {script}")
        WebScraper.random_sleep()


class ChromeFactory:

    @staticmethod
    def create_chrome(path=None, *args, **kwargs):
        """
        Build default Chrome instance.
        """
        if 'version' in kwargs:
            version = kwargs['version']
        else:
            version = 'latest'

        if 'options' in kwargs:
            chrome_options = kwargs['options']
        else:
            chrome_options = ChromeFactory.build_chrome_options()

        if 'headless'in kwargs:
            chrome_options.headless = kwargs['headless']

        if 'chrome_driver_bin' in kwargs:
            chrome_driver_bin = kwargs['chrome_driver_bin']
        else:
            chrome_driver_bin = ChromeDriverManager(version=version, path=path).install()

        driver = webdriver.Chrome(
            executable_path=chrome_driver_bin, options=chrome_options
        )

        driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT_IN_SEC)
        driver.set_script_timeout(SCRIPT_TIMEOUT_IN_SEC)

        # driver_wrapper = ExtendedWebDriver(driver, WebDriverErrorHandler())
        driver_wrapper = EventFiringWebDriver(driver, MyListener())

        return driver_wrapper

    @staticmethod
    def build_chrome_options():

        # https: // sites.google.com / a / chromium.org / chromedriver / capabilities

        chrome_options = webdriver.ChromeOptions()
        chrome_options.accept_untrusted_certs = True
        chrome_options.assume_untrusted_cert_issuer = True
        # chrome configuration
        # More: https://github.com/SeleniumHQ/docker-selenium/issues/89
        # And: https://github.com/SeleniumHQ/docker-selenium/issues/87
        chrome_options.headless = False
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--remote-debugging-port=9222")
        # chrome_options.add_argument("--disable-impl-side-painting")
        # chrome_options.add_argument("--disable-setuid-sandbox")
        # chrome_options.add_argument("--disable-seccomp-filter-sandbox")
        # chrome_options.add_argument("--disable-breakpad")
        # chrome_options.add_argument("--disable-client-side-phishing-detection")
        # chrome_options.add_argument("--disable-cast")
        # chrome_options.add_argument("--disable-cast-streaming-hw-encoding")
        # chrome_options.add_argument("--disable-cloud-import")
        # chrome_options.add_argument("--disable-popup-blocking")
        # chrome_options.add_argument("--ignore-certificate-errors")
        # chrome_options.add_argument("--disable-session-crashed-bubble")
        # chrome_options.add_argument("--disable-ipv6")
        # chrome_options.add_argument("--allow-http-screen-capture")
        # chrome_options.add_argument("--start-maximized")

        # Experimental Options -- These may break chromedriver in future releases
        # Experimental Options used to undefine navigator.webdriver = true
        # Does not work in headless mode.
        # These options avoid bot detection from distil.
        # More info here: https://stackoverflow.com/questions/53039551/selenium-webdriver-modifying-navigator-webdriver-flag-to-prevent-selenium-detec?noredirect=1&lq=1
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        # These options remove password manager
        # chrome_options.add_experimental_option('credentials_enable_service', False)
        # chrome_options.add_experimental_option('profile.password_manager_enabled', False)

        # Testing these options
        # chrome_options.add_experimental_option("excludeSwitches", ['bypass-app-banner-engagement-checks',
        #                                                            'google-password-manager',
        #                                                            'enable-automation'])
        # Add User Preferences
        prefs = {"credentials_enable_service": False}  # Disables password manager
        prefs.update(
            {"profile.password_manager_enabled": False}
        )  # Disables password manager
        chrome_options.add_experimental_option("prefs", prefs)

        # For Heroku
        chrome_bin = os.environ.get("GOOGLE_CHROME_BIN")
        if chrome_bin:
            chrome_options.binary_location = chrome_bin

        return chrome_options

    @staticmethod
    def get_driver_path():

        chrome_driver_folder_name = ""
        if platform == "linux" or platform == "linux2":
            # linux
            chrome_driver_folder_name = "linux_x64"
        elif platform == "darwin":
            # OS X
            chrome_driver_folder_name = "mac_x64"
        else:
            raise ValueError("Platform not identified")

        chrome_driver_path = os.path.normpath(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                os.pardir,
                os.pardir,
                os.pardir,
                "resources",
                "chrome",
                chrome_driver_folder_name,
                "chromedriver",
            )
        )
        assert os.path.isfile(chrome_driver_path), (
            "Chrome driver must exists: %s" % chrome_driver_path
        )

        return chrome_driver_path


class WebScraper:
    def __init__(self):
        self.driver: EventFiringWebDriver = None
        self.logger = logging.getLogger(__name__)
        self.logger.debug("creating an instance of %s", __class__)
        self.implicit_wait_range = IMPLICITLY_WAIT_RANGE
        self.implicit_wait_time = self.randomize_wait_time

    def setup_driver(self, chrome_driver_path=None, *args, **kwargs):
        if chrome_driver_path is None:
            chrome_driver_path = os.environ.get("CHROMEDRIVER_PATH", os.path.abspath("."))

        self.driver = ChromeFactory.create_chrome(path=chrome_driver_path, *args, **kwargs)
        self.logger.info("Chromedriver Online.")
        self.logger.debug(
            f"Setting Driver Implicit wait time to: {self.implicit_wait_time}"
        )
        self.driver.implicitly_wait(self.implicit_wait_time)

    @property
    def randomize_wait_time(self):
        return random.uniform(*self.implicit_wait_range)

    @staticmethod
    def random_sleep(sleep_range: Tuple[int, int] = (5, 10)) -> None:
        sleep_time = random.uniform(*sleep_range)
        time.sleep(sleep_time)

    def teardown_driver(self):
        self.driver.quit()
        self.logger.info("Driver Offline")

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
        url = "https://ipleak.net/"
        xpath = "/html/body/div/div[3]/div[10]/div[1]/table/tbody/tr[1]/td[2]"
        text = "Chrome"
        self.driver.get(url)
        try:
            WebDriverWait(self.driver, 20).until(
                EC.text_to_be_present_in_element((By.XPATH, xpath), text)
            )
            self.logger.info("Page Loaded.")
        except Exception as e:
            self.logger.error(e)

        if self.driver.page_source.find("HeadlessChrome") > 0:
            self.logger.info(
                "Your browser is currently being detected as headless, "
                "reconfigure your options or run headless=False"
            )
        else:
            self.logger.info("Your headless browser has not been detected. :)")

    def wait(self, wait_time=20, **kwargs):
        """ Wrapper for WebDriverWait """
        wait = WebDriverWait(self.driver, wait_time, **kwargs)
        return wait

    def explicit_wait(self, selector, element_name, wait_time=10):
        """ Wrapper for explicit waits. Function waits until the element appears on the page; if element does not appear
        after wait_time an exception is raised.

        :param selector: Locator for element. For Convenience use the By class in selenium.webdriver.common.by for passing selector methods.
        :param element_name: Name of the element for which the locator searchs.
        :param wait_time: Amount of time to wait before exception
        :return: Element
        """
        try:
            return self.wait(wait_time).until(
                EC.presence_of_element_located((selector, element_name))
            )
        except TimeoutException:
            self.logger.error(
                f"{element_name} not found at {selector} on {self.driver.title}. Timeout after {wait_time}"
            )
            raise TimeoutException

    def save_screenshot(self, filename: str = None) -> None:
        """ Saves a .png screen shot to relative screenshots folder.
        :param filename: String name for local file. If empty, will be the title of current url.
        """

        screenshots_dir = "screenshots"
        if filename is None:
            title = self.driver.title.split(" ")
            if len(title) > 2:
                filename = "".join(self.driver.title.split(" ")[:2])
            else:
                filename = title

        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)

        relative_file_path = os.path.join(screenshots_dir, filename)
        self.driver.save_screenshot(f"{relative_file_path}.png")
        self.logger.info(f"Saved Screenshot to {relative_file_path}.png")

    def _js_inject_js(self, js=None, is_async=False, *args):
        if is_async:
            self.driver.execute_async_script(js, *args)
        else:
            self.driver.execute_script(js, *args)

    def js_scroll_into_view(self, element):
        # Uses Javascript to scroll an element into view.
        self.logger.debug("Scrolling element into view")
        js = "arguments[0].scrollIntoView();"
        try:
            self._js_inject_js(js, False, element)
        except Exception as e:
            self.logger.error("Element not found?\n %s", e)
            raise e

    def js_scroll_to_bottom(self):
        # Scrolls to bottom of page. Good for inifinite feeds like FB or twitter.
        self.logger.debug("Scrolling window to bottom...")
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def js_get_page_state(self):
        """
        Javascript for getting document.readyState
        :return: Pages state.

        More Info: https://developer.mozilla.org/en-US/docs/Web/API/Document/readyState
        """
        ready_state = self.driver.execute_script("return document.readyState")
        if ready_state == "loading":
            self.logger.debug("Loading Page...")
        elif ready_state == "interactive":
            self.logger.debug("Page is interactive")
        elif ready_state == "complete":
            self.logger.debug("The page is fully loaded!")
        return ready_state

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
        self.logger.info(
            f"{len(set(links))} unique links collected from {self.driver.title}"
        )
        return set(links)

    def random_move_mouse(self):
        # Imitate human mouse movements with bspline movements.
        pass
        # action = ActionChains(self.driver)
        #
        # startElement = self.driver.find_element_by_id("//a[href]")
        #
        # # First, go to your start point or Element
        # action.move_to_element_with_offset(startElement, 0, 0)
        # action.perform()
        #
        # for mouse_x, mouse_y in get_bspline():
        #     action.move_by_offset(mouse_x, mouse_y)
        #     action.perform()
        #     self.random_sleep(sleep_range=(0, 0.05))
        #     print(mouse_x, mouse_y)

    def test_distil_bot_detection(self):
        # This website has distil technology.
        # A good test website to see if we can bypass bot detection
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
        # Also another website to test for bot detection.
        # TODO: After submitting search we should check for captchas, if not we are good!
        if self.driver is None:
            self.setup_driver()

        self.driver.get("https://www.google.com")
        search_element = self.driver.find_element_by_name("q")
        self.random_send_keys("cats", search_element)
        search_element.submit()

    def random_send_keys(self, keys, element):
        """
        Randomizes Sleep between key sends for element.
        """
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

    def login_and_authenticate(self, login_btn, username_element, password_element, username, password):
        current_url = self.driver.current_url
        self.random_send_keys(element=username_element, keys=username)
        self.random_send_keys(element=password_element, keys=password)
        # login_btn = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Login')]")
        # submit_btn = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Sign in')]")
        login_btn.click()
        # Wait for url to change to confirm login.
        self.logger.info("Logging in...")
        count = 0
        while current_url == self.driver.current_url:
            if count > SCRIPT_TIMEOUT_IN_SEC:
                raise TimeoutException
            time.sleep(1)
            count += 1
        self.logger.info("Succesfully Logged in.")

    def random_element_rect(self):
        # function for moving the mouse to a random starting position on the page.
        # Returns dictionary of random element size and location
        action = ActionChains(self.driver)
        start_elements = self.driver.find_elements_by_id("//a[href]")
        random_start_element = start_elements[random.randint(0, len(start_elements))]
        action.move_to_element_with_offset(random_start_element, 0, 0)
        action.perform()

        return random_start_element.rect

    def get_info(self) -> Dict:
        info = {'title': self.driver.title,
                'url': self.driver.current_url,
                'page_source': self.driver.page_source,
                'current_tab': self.driver.current_window_handle,
                'user_data_dir': self.driver.capabilities['chrome']['userDataDir'],
                'browserVersion': self.driver.capabilities['chrome']['browserVersion'],
                'platformName': self.driver.capabilities['platformName'],
                }

        return info

    def __del__(self):
        self.teardown_driver()
