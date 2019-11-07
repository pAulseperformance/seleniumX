import os
from webdriver_manager.chrome import ChromeDriverManager
import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

webdriver.Chrome(ChromeDriverManager().install())