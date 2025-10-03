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

# 2 - mudar a cor pra "verde"
green_color_element = driver.find_element("-android uiautomator", 'new UiSelector().description("Green color")')
green_color_element.click()
time.sleep(1)

# 3 - aumentar a quantidade pra 2
select_product_plus = driver.find_element("-android uiautomator", 'new UiSelector().resourceId("com.saucelabs.mydemoapp.android:id/plusIV")')
select_product_plus.click()
time.sleep(1)

# 4 - adicionar ao carrinho
button_add_to_cart = driver.find_element("-android uiautomator", 'new UiSelector().resourceId("com.saucelabs.mydemoapp.android:id/cartBt")')
button_add_to_cart.click()
time.sleep(2)

# 5 - abrir o carrinho
button_open_cart = driver.find_element("-android uiautomator", 'new UiSelector().resourceId("com.saucelabs.mydemoapp.android:id/cartIV")')
button_open_cart.click()
time.sleep(4)

# 6 - no carrinho, diminuir a quantidade para 1
select_product_minus = driver.find_element("-android uiautomator", 'new UiSelector().resourceId("com.saucelabs.mydemoapp.android:id/minusIV")')
select_product_minus.click()
time.sleep(1)

# 7 - prosseguir para o checkout
button_proceed_to_checkout = driver.find_element("-android uiautomator", 'new UiSelector().resourceId("com.saucelabs.mydemoapp.android:id/cartBt")')
button_proceed_to_checkout.click()
time.sleep(4)

# 8 - na tela de login, preencher "UserTest"
login_text_field = driver.find_element("-android uiautomator", 'new UiSelector().resourceId("com.saucelabs.mydemoapp.android:id/nameET")')
login_text_field.send_keys(login)
time.sleep(1)

# 9 - preencher "PasswordTest"
password_text_field = driver.find_element("-android uiautomator", 'new UiSelector().resourceId("com.saucelabs.mydemoapp.android:id/passwordET")')
password_text_field.send_keys(password)
time.sleep(1)

# 10 - clicar em login
button_login = driver.find_element("-android uiautomator", 'new UiSelector().resourceId("com.saucelabs.mydemoapp.android:id/loginBtn")')
button_login.click()
time.sleep(4)

# 11 - na tela de checkout, preencher name
name_text_field = driver.find_element("-android uiautomator", 'new UiSelector().resourceId("com.saucelabs.mydemoapp.android:id/fullNameET")')
name_text_field.send_keys(fullName)
time.sleep(1)

# 12 - preencher address line 1
address_one_text_field = driver.find_element("-android uiautomator", 'new UiSelector().resourceId("com.saucelabs.mydemoapp.android:id/address1ET")')
address_one_text_field.send_keys(addressLine1)
time.sleep(1)

# 13 - preencher address line 2
adress_two_text_field = driver.find_element("-android uiautomator", 'new UiSelector().resourceId("com.saucelabs.mydemoapp.android:id/address2ET")')
adress_two_text_field.send_keys(addressLine2)
time.sleep(1)

 # 14 - preencher city
city_text_field = driver.find_element("-android uiautomator", 'new UiSelector().resourceId("com.saucelabs.mydemoapp.android:id/cityET")')
city_text_field.send_keys(city)
time.sleep(1)

# 15 - preencher state/region
state_text_field = driver.find_element("-android uiautomator", 'new UiSelector().resourceId("com.saucelabs.mydemoapp.android:id/stateET")')
state_text_field.send_keys(stateRegion)
time.sleep(1)

# 16 - preencher zip code
zip_text_field = driver.find_element("-android uiautomator", 'new UiSelector().resourceId("com.saucelabs.mydemoapp.android:id/zipET")')
zip_text_field.send_keys(zipCode)
time.sleep(1)

 # 17 - preencher country
country_text_field = driver.find_element("-android uiautomator", 'new UiSelector().resourceId("com.saucelabs.mydemoapp.android:id/countryET")')
country_text_field.send_keys(country)
time.sleep(1)

# 18 - clicar em prosseguir para o pagamento
button_to_payment = driver.find_element("-android uiautomator", 'new UiSelector().resourceId("com.saucelabs.mydemoapp.android:id/paymentBtn")')
button_to_payment.click()
time.sleep(4)

# 19 - na tela de pagamento, preencher name on card
card_full_name_text_field = driver.find_element("-android uiautomator", 'new UiSelector().resourceId("com.saucelabs.mydemoapp.android:id/nameET")')
card_full_name_text_field.send_keys(cardFullName)
time.sleep(1)

# 20 - preencher card number
card_number_text_field = driver.find_element("-android uiautomator", 'new UiSelector().resourceId("com.saucelabs.mydemoapp.android:id/cardNumberET")')
card_number_text_field.send_keys(cardNumber)
time.sleep(1)

# 21 - preencher expiration date
expiration_date_text_field = driver.find_element("-android uiautomator", 'new UiSelector().resourceId("com.saucelabs.mydemoapp.android:id/expirationDateET")')
expiration_date_text_field.send_keys(expirationDate)
time.sleep(1)

# 22 - preencher security code
security_code_text_field = driver.find_element("-android uiautomator", 'new UiSelector().resourceId("com.saucelabs.mydemoapp.android:id/securityCodeET")')
security_code_text_field.send_keys(securityCode)
time.sleep(1)

# 23 - clicar em prosseguir
button_review_order = driver.find_element("-android uiautomator", 'new UiSelector().resourceId("com.saucelabs.mydemoapp.android:id/paymentBtn")')
# com.saucelabs.mydemoapp.android:id/paymentBtn id
# "Saves payment info and launches screen to review checkout data" accessibility id
button_review_order.click()
time.sleep(4)

# 24 - na tela de checkout, clicar em prosseguir
button_place_order = driver.find_element("-android uiautomator", 'new UiSelector().resourceId("com.saucelabs.mydemoapp.android:id/paymentBtn")')
# com.saucelabs.mydemoapp.android:id/paymentBtn id
# "Completes the process of checkout" accessibility id
button_place_order.click()
time.sleep(4)

# 25 - ao estar na tela de "Checkout Complete", verificar se o elemento "completeTV" está presente
elements = driver.find_elements(
    AppiumBy.ANDROID_UIAUTOMATOR,
    'new UiSelector().resourceId("com.saucelabs.mydemoapp.android:id/completeTV")'
)
if elements:
    print("✅ Elemento está na tela, compra foi concluída!")
else:
    print("❌ Elemento NÃO encontrado, tem problema aí mermão")

driver.quit()