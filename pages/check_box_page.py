from selenium.webdriver.common.by import By

class CheckBoxPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://demoqa.com/checkbox"
        # Locators       
        self.expand_all_button = (By.CSS_SELECTOR, "button[title='Expand all']")
        self.commands_checkbox = (By.XPATH, "//label[@for='tree-node-commands']")
        self.commands_input = (By.ID, "tree-node-commands")

    def expand_all_click(self):
        self.driver.find_element(*self.expand_all_button).click()

    def navigate(self):
        self.driver.get(self.url)

    ## NOTES
    def notes_checkbox_click(self):
        self.notes_checkbox = self.driver.find_element(By.ID, "tree-node-notes")
        self.notes_checkbox.click()

    def notes_checkbox_output(self):
        self.notes_input = self.driver.find_element(By.ID, "tree-node-notes")
        return self.notes_input


    ## COMMANDS
    def commands_checkbox_click(self):   
        self.driver.find_element(*self.commands_checkbox).click()

    # def check_commands_input(self):
    #     return self.driver.find_element(By.ID, "tree-node-commands").is_selected()

    def commands_checkbox_output(self):
        return self.driver.find_element(*self.commands_input).is_selected()
        