from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TooltipsPage:
    """Page Object Model do Tooltips Page.
    Retorna:
    - Navigate: navega para a URL do Tooltips Page.
    - Tooltip Button Hover: passa o mouse sobre o botão de modo à mostrar o tooltip.
    - Tooltip Button Hover Text: retorna o texto do tooltip do botão.
    - Tooltip Text Field Hover: passa o mouse sobre o campo de texto de modo à mostrar o tooltip.
    - Tooltip Text Field Hover Text: retorna o texto do tooltip do campo de texto."""
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://demoqa.com/tool-tips"
        self.actions = ActionChains(self.driver)
        self.wait = WebDriverWait(self.driver, 10)

        # Locators       
        self.tool_tip_button = (By.ID, "toolTipButton")
        self.tool_tip_text_field = (By.ID, "toolTipTextField")
        self.text_field_hover_tooltip_w = (By.ID, "textFieldToolTip")
        self.button_hover_tooltip_w = (By.ID, "buttonToolTip")

    def navigate(self, url):
        self.driver.get(url)

    # button
    def tooltip_button_hover(self):
        button = self.driver.find_element(*self.tool_tip_button)
        self.actions.move_to_element(button).perform()

    def tooltip_button_hover_text(self):
        button_hover_tooltip = self.wait.until(EC.visibility_of_element_located(self.button_hover_tooltip_w))
        return button_hover_tooltip.text
    
    # text field
    def tooltip_text_field_hover(self):
        text_field = self.driver.find_element(*self.tool_tip_text_field)
        self.actions.move_to_element(text_field).perform()

    def tooltip_text_field_hover_text(self):
        text_field_hover_tooltip = self.wait.until(EC.visibility_of_element_located(self.text_field_hover_tooltip_w))
        return text_field_hover_tooltip.text