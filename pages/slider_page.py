from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

class SliderPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://demoqa.com"
        self.wait = WebDriverWait(self.driver, 10)
        
        # Locators  
        self.alerts_home_button = (By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div[4]/div/div[1]") # por ID e CSS Selector não funcionou
        self.alerts_button = (By.XPATH, "/html/body/div[2]/div/div/div/div[1]/div/div/div[4]/div/ul/li[4]") # por ID e CSS Selector não funcionou
        self.slider_handle = (By.CSS_SELECTOR, "input[type='range']") # não consegui por ID

    def navigate(self):
        self.driver.get(self.url)
    
    #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

    # Test case: DemoQA homepage
    # 1 - abrir homepage
    # 2 - clicar em "Widgets"
    def open_widgets_page_from_home(self):
        self.driver.find_element(*self.alerts_home_button).click() # 2 por XPATH
    
    #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

    # Test case: slider page
    # 3 - clicar em "slider"
    def open_slider_page(self):
        self.driver.find_element(*self.alerts_button).click() # 3 por XPATH
    
    #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

    # Test case: selecionar valor do slider
    # 4 - mover o slider para o valor selecionado
    # 5 - checar se o valor do slider é o mesmo que o selecionado
    def set_slider_value(self, value):
        slider = self.driver.find_element(*self.slider_handle)
        action = ActionChains(self.driver)
        action.click_and_hold(slider).move_by_offset(value - int(slider.get_attribute("value")), 0).release().perform() # 4
        slider_value = int(slider.get_attribute("value")) # salvar valor do slider em variável
        return slider_value # 5
    
    #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#


    
    #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

