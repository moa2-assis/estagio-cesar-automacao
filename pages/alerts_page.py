from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AlertsPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://demoqa.com"
        self.wait = WebDriverWait(self.driver, 10)
        
        # Locators  
        self.alerts_home_button = (By.XPATH, "//*[@id='app']/div/div/div[2]/div/div[3]/div") # por ID e CSS Selector não funcionou
        self.alerts_button = (By.XPATH, "/html/body/div[2]/div/div/div/div[1]/div/div/div[3]/div/ul/li[2]") # por ID e CSS Selector não funcionou
        self.alert_page_button = (By.ID, "alertButton")
        self.alert_page_timer_button = (By.ID, "timerAlertButton")
        self.alert_page_confirm_button = (By.ID, "confirmButton")
        self.alert_page_confirm_output = (By.ID, "confirmResult")
        self.alert_page_prompt_button = (By.ID, "promtButton")
        self.alert_page_prompt_output = (By.ID, "promptResult")

    def navigate(self):
        self.driver.get(self.url)
    
    #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

    # Test case: DemoQA homepage
    # 1 - abrir homepage
    # 2 - clicar em "Alerts, Frames & Windows"
    def open_alerts_page_from_home(self):
        self.driver.find_element(*self.alerts_home_button).click() # 2 por XPATH
    
    #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

    # Test case: alerts page
    # 3 - clicar em "Alerts"
    def open_alerts_page(self):
        self.driver.find_element(*self.alerts_button).click() # 3 por XPATH
    
    #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

    # Test case: click to see alert
    # 4 - clicar no primeiro botão "Click me"
    # 5 - checar se houve um alerta aberto
    # 6 - comparar o texto do alerta com "You clicked a button"
    def click_to_see_alert(self):
        self.driver.find_element(*self.alert_page_button).click() # 4 por ID
        alert = self.wait.until(EC.alert_is_present()) # 5
        alert_text = alert.text # salvar texto do alerta em variável
        alert.accept()
        return alert_text # 6
    
    #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

    # Test case: click to see alert after 5 seconds
    # 7 - clicar no segundo botão "Click me"
    # 8 - checar se houve um alerta aberto após 5 segundos
    # 9 - comparar o texto do alerta com "This alert appeared after 5 seconds
    def click_to_see_alert_after_5_seconds(self):
        self.driver.find_element(*self.alert_page_timer_button).click() # 7 por ID
        alert = self.wait.until(EC.alert_is_present()) # 8
        alert_text = alert.text # salvar texto do alerta em variável
        alert.accept() # confirmar alerta
        return alert_text # 9
    
    #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

    # Test case: button confirm
    # 10 - clicar no terceiro botão "Click me"
    # 11 - checar se houve um alerta aberto
    # 12 - clicar em "OK"
    # 13 - comparar o texto exibido na página com "You selected Ok"
    # 14 - clicar no terceiro botão "Click me"
    # 15 - checar se houve um alerta aberto
    # 16 - clicar em "Cancelar"
    # 17 - comparar o texto exibido na página com "You selected Cancel"
    def button_confirm(self, accept=True):
        self.driver.find_element(*self.alert_page_confirm_button).click() # 10 e 14 por ID
        alert = self.wait.until(EC.alert_is_present()) # 11 e 15
        if accept:
            alert.accept() # 12
        else:
            alert.dismiss() # 16
        result_text = self.driver.find_element(*self.alert_page_confirm_output).text # salvar texto do alerta em variável
        return result_text # 13 e 17
    
    #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

    # Test case: button prompt message
    # 18 - scrollar para o quarto botão "Click me"
    # 19 - clicar no quarto botão "Click me"
    # 20 - checar se houve um alerta aberto
    # 21 - digitar "Mateuzo" no campo do alerta
    # 22 - clicar em "OK"
    # 23 - comparar o texto exibido na página com "You entered Mateuzo"
    def button_prompt_message(self, message):
        scroll_to_prompt_button = self.driver.find_element(*self.alert_page_prompt_button)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", scroll_to_prompt_button) # 18 por ID salvo em variável auxiliar para SCROLLAR
        self.driver.find_element(*self.alert_page_prompt_button).click() # 19 por ID
        alert = self.wait.until(EC.alert_is_present()) # 20
        alert.send_keys(message) # 21
        alert.accept() # 22
        result_text = self.driver.find_element(*self.alert_page_prompt_output).text # salvar texto do alerta em variável
        return result_text # 23