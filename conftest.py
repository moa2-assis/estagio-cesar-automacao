# conftest.py
import pytest
from selenium import webdriver

@pytest.fixture
def driver():
    # Setup: initialize the WebDriver
    driver = webdriver.Chrome()
    # driver = webdriver.Firefox()
    driver.maximize_window()
    yield driver

    # Teardown: close the WebDriver
    driver.quit()