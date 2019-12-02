from seleniumX.scraper import WebScraper
from selenium.webdriver.support import expected_conditions as EC


url = 'https://www.google.com'

# Instantiate the class which wraps selenium webdriver base class, with an event listener for debugging
# and an automatic webdriver manager
ws = WebScraper()
# Setup_driver takes care of downloading the latest chrome binary. You must call this to start the chrome browser.
# By default, setup_driver will look for the path to the chrome binary first in an environment variable CHROMEDRIVER_PATH
# This variable is specific to Heroku deployments. If that is not set, it will download the
# latest chrome binary and save it to the project root directory.
# The browser will also not be headless.
ws.setup_driver()

# To override the defaults simply pass it keyword arguments.
# ws.setup_driver(chrome_driver_path='/absolute/path/to/a/directory/to/save/chromedriver/in',
#                 headless=True,
#                 version="2.26")

# If you want to setup a driver the old fashioned way, then you can point to an already installed version of chromedriver to use
# ws.setup_driver(chrome_driver_bin='/absolute/path/to/a/directory/to/save/chromedriver/in/chromedriver')

# ws.setup_driver(chrome_driver_bin='/Users/home/PycharmProjects/seleniumX/seleniumX/drivers/drivers/chromedriver/2.26/mac64/chromedriver')
ws.driver.get(url)

# Avoid bot detections
ws.random_sleep()  # Default is 5 - 10 seconds
ws.random_sleep(sleep_range=(1, 2))  # or you can pass a tuple of a different range.

# Access the driver like normal.
element = ws.driver.find_element_by_name("q")

# Use random key inputs to prevent bot detection
ws.random_send_keys("Hello World", element)
# lucky_btn = ws.driver.find_element_by_name("btnI")
search_btn = ws.driver.find_element_by_name("btnK")
search_btn.click()

# Shortened Webdriver wait class.
ws.wait().until(EC.title_contains("Hello World"))

# Quickly grab all the unique links from a webpage
unique_links = ws.get_all_unique_links()
print(unique_links)

# Js Functions
# element = ws.driver.find_element_by_name('g')
ws.js_scroll_to_bottom()
# ws.js_scroll_into_view(element)

# Save a screenshot, by default will take the page title name as filename
ws.save_screenshot()
# Or pass it a filename
ws.save_screenshot("Googlesearchresults")

# Returns various info about the driver and page.
info = ws.get_info()
print(info)

# ws.driver.execute_script("document.getElementById('recaptcha-anchor').click()")