import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

class SliderPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://demoqa.com"
        self.wait = WebDriverWait(self.driver, 10)
        
        # Locators  
        self.widgets_home_button = (By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div[4]/div") # por ID e CSS Selector não funcionou
        self.slider_button = (By.XPATH, "/html/body/div[2]/div/div/div/div[1]/div/div/div[4]/div/ul/li[4]") # por ID e CSS Selector não funcionou
        self.slider_handle = (By.XPATH, "/html/body/div[2]/div/div/div/div[2]/form/div/div[1]/span/input") # não consegui por ID

    def navigate(self):
        self.driver.get(self.url)
    
    #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

    # Test case: DemoQA homepage
    # 1 - abrir homepage
    # 2 - clicar em "Widgets"
    def open_widgets_page_from_home(self):
        self.driver.find_element(*self.widgets_home_button).click() # 2 por XPATH
    
    #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

    # Test case: slider page
    # 3 - scrollar até o botão "slider"
    # 4 - clicar em "slider"
    def open_slider_page(self):
        scroll_to_slider = self.driver.find_element(*self.slider_button)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", scroll_to_slider) 
        self.driver.find_element(*self.slider_button).click() # 3 por XPATH
    
    #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

    # Test case: selecionar valor do slider
    # 5 - mover o slider para o valor selecionado pressionando seta pro lado direito/esquerdo após deixá-la "focused"
    def set_slider_value_while(self, value):
        slider = self.driver.find_element(*self.slider_handle)
        ActionChains(self.driver).move_to_element_with_offset(slider, 1, 0).click_and_hold().move_by_offset(5, 0).release().perform()
        current_value = int(slider.get_attribute("value"))
        while current_value != value:
            if current_value < value:
                slider.send_keys(Keys.ARROW_RIGHT)
                current_value += 1
            else:
                slider.send_keys(Keys.ARROW_LEFT)
                current_value -= 1

        time.sleep(2)
    
    #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

    # Test case: selecionar valor do slider
    # 6 - checar se o valor do slider é o mesmo que o selecionado
    def get_slider_value(self):
        slider = self.driver.find_element(*self.slider_handle)
        slider_value = int(slider.get_attribute("value")) # salvar valor do slider em variável
        return slider_value
    
    #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

