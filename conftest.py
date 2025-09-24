import pytest
from selenium import webdriver
import json
from pathlib import Path

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="browser to execute tests (chrome or firefox)")

@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser").lower()
    if browser == "chrome":
        driver_instance = webdriver.Chrome()
    elif browser == "firefox":
        driver_instance = webdriver.Firefox()
    else:
        raise ValueError(f"Browser '{browser}' is not supported.")
    
    driver_instance.maximize_window()
    yield driver_instance
    driver_instance.quit()

# Fixture to load test data from JSON
@pytest.fixture(scope="session")
def test_data():
    with open("data/test_data.json") as f:
        return json.load(f)

LOG_FILE = Path("test_durations.log")