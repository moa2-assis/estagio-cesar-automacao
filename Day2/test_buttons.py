from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

def test_double_click_button(driver):
    driver.get("https://demoqa.com/buttons")
    doubleclick_button = driver.find_element(By.ID, "doubleClickBtn")
    actions = ActionChains(driver)
    actions.double_click(doubleclick_button).perform()
    time.sleep(2)
    output_msg_element = driver.find_element(By.ID, "doubleClickMessage")
    assert "You have done a double click" in output_msg_element.text

def test_right_click_button(driver):
    driver.get("https://demoqa.com/buttons")
    rightclick_button = driver.find_element(By.ID, "rightClickBtn")
    actions = ActionChains(driver)
    actions.context_click(rightclick_button).perform()
    time.sleep(2)
    output_msg_element = driver.find_element(By.ID, "rightClickMessage")
    assert "You have done a right click" in output_msg_element.text

def test_dynamic_click_button(driver):
    driver.get("https://demoqa.com/buttons")
    dynamicclick_button = driver.find_element(By.XPATH, "//button[text()='Click Me']")
    dynamicclick_button.click()
    time.sleep(2)
    output_msg_element = driver.find_element(By.ID, "dynamicClickMessage")
    time.sleep(2)
    assert "You have done a dynamic click" in output_msg_element.text

