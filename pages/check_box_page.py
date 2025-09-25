from selenium.webdriver.common.by import By

class CheckBoxPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://demoqa.com/checkbox"
        # Locators       
        self.expand_all_button = (By.CSS_SELECTOR, "button[title='Expand all']")
        self.commands_checkbox = (By.XPATH, "//label[@for='tree-node-commands']")
        self.commands_input = (By.ID, "tree-node-commands")
        self.notes_checkbox = (By.XPATH, "//label[@for='tree-node-notes']")
        self.notes_input = (By.ID, "tree-node-notes")

    def expand_all_click(self):
        self.driver.find_element(*self.expand_all_button).click()

    def navigate(self):
        self.driver.get(self.url)

    ## COMMANDS
    def commands_checkbox_click(self):   
        self.driver.find_element(*self.commands_checkbox).click()

    def commands_checkbox_output(self):
        commands = self.driver.find_element(*self.commands_input).is_selected()
        return commands
        
    ## NOTES
    def notes_checkbox_click(self):
        self.driver.find_element(*self.notes_checkbox).click()

    def notes_checkbox_output(self):
        notes = self.driver.find_element(*self.notes_input).is_selected()
        return notes