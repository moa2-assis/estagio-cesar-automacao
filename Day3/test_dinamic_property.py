import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_dinamic_button(driver):

    driver.get("https://demoqa.com/elements")

    dynamic_property = driver.find_element(By.ID, "item-8")
    
    driver.execute_script("arguments[0].scrollIntoView(true);", dynamic_property)

    assert dynamic_property.is_displayed()
    dynamic_property.click()
    
    wait = WebDriverWait(driver, 10)

    visible_After_button = wait.until(
        EC.element_to_be_clickable((By.ID, "visibleAfter"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", dynamic_property)
    visible_After_button.click()