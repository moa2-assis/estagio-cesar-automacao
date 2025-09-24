from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

class TooltipsPage2:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://demoqa.com/tool-tips"
        self.actions = ActionChains(self.driver)

        # Locators       
        self.tool_tip_button = (By.ID, "toolTipButton")
        self.tool_tip_text_field = (By.ID, "toolTipTextField")

    def navigate(self):
        self.driver.get(self.url)

    # button
    def tool_tip_button_hover(self):
        button = self.driver.find_element(*self.tool_tip_button)
        self.actions.move_to_element(button).perform()

    def tool_tip_button_hover_tooltip_text(self):
        button_hover_tooltip = self.driver.find_element(By.ID, "buttonToolTip")
        return button_hover_tooltip.text
    
    # text field
    def tool_tip_text_hover(self):
        text_field = self.driver.find_element(*self.tool_tip_text_field)
        self.actions.move_to_element(text_field).perform()

    def tool_tip_text_field_hover_text(self):
        text_field_hover_tooltip = self.driver.find_element(By.ID, "textFieldToolTip")
        return text_field_hover_tooltip.text