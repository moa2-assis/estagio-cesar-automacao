import pytest
import pytest_html
from selenium import webdriver
import json
from pathlib import Path
import time
import os, pytest_html
from datetime import datetime
import sys
import subprocess
import webbrowser

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

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    item.start_time = time.time()
    item.start_str = time.strftime("%H:%M:%S", time.localtime())
    msg = f"\n[START] Test '{item.nodeid}' - {item.start_str}"
    print(msg)
    
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(msg + "\n")

@pytest.hookimpl(trylast=True)
def pytest_runtest_teardown(item):
    duration = time.time() - item.start_time
    msg = f"[END] Test '{item.nodeid}' finished in {duration:.2f} seconds."
    print(msg)

    # salva em arquivo
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(msg + "\n")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])
    if report.when == "call" and report.failed:
        # Create screenshots directory if it doesn't exist
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
        # Take screenshot
        driver = item.funcargs['driver']
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        browserName = driver.capabilities.get("browserName", "unknown").lower()
        screenshot_file = os.path.join("screenshots", f"{timestamp}_{item.name}_error_{browserName}_.png")
        driver.save_screenshot(screenshot_file)
        # Add screenshot to the HTML report
        if screenshot_file:
            html = f'<div><img src="{screenshot_file}" alt="screenshot" style="width:304px;height:228px;" ' \
           f'onclick="window.open(this.src)" align="right"/></div>'
            extra.append(pytest_html.extras.html(html))
    report.extra = extra

def pytest_sessionfinish(session, exitstatus):
    root = Path.cwd()
    script = root / "dashboard.py"
    html   = root / "dashboard.html"

    try:
        subprocess.run([sys.executable, str(script)], check=True)
    except Exception as e:
        print(f"[dashboard] erro ao executar {script.name}: {e}")
        return

    try:
        webbrowser.open(html.resolve().as_uri())
    except Exception as e:
        print(f"[dashboard] gerado em: {html.resolve()} (abra manualmente). Motivo: {e}")