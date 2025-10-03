import time
from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy

# Starts the application.
# Selects the first item from the product list.
# Changes the color to Green.
# Increases the quantity to 2.
# Adds to cart.
# Opens the cart.
# In the cart, decreases the quantity to 1.
# Proceeds to checkout.
# On the Login screen, enters "UserTest" and "PasswordTest" and logs in.
# On the Checkout screen, fills in all values and proceeds.
# On the Payment screen, fills in all data and proceeds.
# On the Checkout screen, just proceeds.
# Enters the "Checkout Complete" screen.

login = "UserTest"
password = "PasswordTest"

fullName = "Mateuzo Azzis"
addressLine1 = "Rua dos mamãos"
addressLine2 = "casa duzentos e 3"
city = "Ali de Lado"
stateRegion = "Centrinho"
zipCode = "2789172891237168958723"
country = "Brasilsilsilsil"

cardFullName = "Mateuzo Azzis"
cardNumber = "1234 1234 1234 1234"
expirationDate = "01/12"
securityCode = "999"


options = AppiumOptions()
options.load_capabilities({
	"platformName": "Android",
	"appium:deviceName": "emulator-5554",
	"appium:automationName": "UiAutomator2",
	"appium:appPackage": "com.saucelabs.mydemoapp.android",
	"appium:ensureWebviewsHavePages": True,
	"appium:nativeWebScreenshot": True,
	"appium:newCommandTimeout": 3600,
	"appium:connectHardwareKeyboard": True,
    "appWaitActivity": "com.saucelabs.mydemoapp.android.view.activities.MainActivity",
    "appWaitDuration": 30000  # opcional, tempo de espera em ms (30s)
})

driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
time.sleep(4)

# 1 - selecionar o primeiro item da lista
first_element_on_backpack_list = driver.find_element("-android uiautomator",'new UiSelector().resourceId("com.saucelabs.mydemoapp.android:id/productIV").instance(0)')
first_element_on_backpack_list.click()
time.sleep(4)

# 4 - adicionar ao carrinho
button_add_to_cart = driver.find_element("-android uiautomator", 'new UiSelector().resourceId("com.saucelabs.mydemoapp.android:id/cartBt")')
button_add_to_cart.click()
time.sleep(4)

# 5 - abrir o carrinho
button_open_cart = driver.find_element("-android uiautomator", 'new UiSelector().resourceId("com.saucelabs.mydemoapp.android:id/cartIV")')
button_open_cart.click()
time.sleep(4)

# 7 - prosseguir para o checkout
button_proceed_to_checkout = driver.find_element("-android uiautomator", 'new UiSelector().resourceId("com.saucelabs.mydemoapp.android:id/cartBt")')
button_proceed_to_checkout.click()
time.sleep(4)

# 8 - na tela de login, clicar em "alice@example.com (locked out)"
locked_out_user = driver.find_element("-android uiautomator", 'new UiSelector().resourceId("com.saucelabs.mydemoapp.android:id/username2TV")')
locked_out_user.click()
time.sleep(4)

# 10 - clicar em login
button_login = driver.find_element("-android uiautomator", 'new UiSelector().resourceId("com.saucelabs.mydemoapp.android:id/loginBtn")')
button_login.click()
time.sleep(4)

# 11 - verificar se a mensagem de erro "Sorry, this user has been locked out." está presente
error_message_elements = driver.find_elements("-android uiautomator", 'new UiSelector().resourceId("com.saucelabs.mydemoapp.android:id/passwordErrorTV")')


if error_message_elements:
    print("✅ Elemento está na tela e usuário foi bloqueado, teste passou")
else:
    print("❌ Elemento NÃO encontrado, tem problema aí mermão")

driver.quit()