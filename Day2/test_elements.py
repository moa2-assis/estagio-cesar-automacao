from selenium.webdriver.common.by import By
import time

def test_navigate_to_elements_page(driver):
    """Navega para a página de elementos."""
    driver.get("https://demoqa.com/elements")
    assert "elements" in driver.current_url

def test_locate_by_id(driver):
    driver.get("https://demoqa.com/elements")
    element = driver.find_element(By.ID, "item-0")
    time.sleep(1)
    assert element.is_displayed()
    assert element.text == "Text Box"

def test_locate_by_css_selector(driver):
    driver.get("https://demoqa.com/elements")
    element = driver.find_element(By.CSS_SELECTOR, "#item-0")
    time.sleep(1)
    assert element.is_displayed()

def test_locate_by_xpath(driver):
    driver.get("https://demoqa.com/elements")
    # A more specific XPath to avoid ambiguity
    element = driver.find_element(By.XPATH, "//span[text()='Text Box']")
    time.sleep(1)
    assert element.is_displayed()