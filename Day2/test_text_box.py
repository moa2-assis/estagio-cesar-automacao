from selenium.webdriver.common.by import By
import time

def test_fill_text_box_form_and_validate(driver):
    driver.get("https://demoqa.com/text-box")

    # Fill out the form
    full_name_input = driver.find_element(By.ID, "userName")
    email_input = driver.find_element(By.ID, "userEmail")
    current_address_input = driver.find_element(By.ID, "currentAddress")
    permanent_address_input = driver.find_element(By.ID, "permanentAddress")
    submit_button = driver.find_element(By.ID, "submit")

    # Test data for the form
    full_name = "Rodrigo"
    email = "rgpe@cesar.org.br"
    current_address = "Rua Barão de Souza Leão, s/n"
    permanent_address = "Avenida Boa Viagem, s/n"

    # Fill the form
    full_name_input.send_keys(full_name)
    email_input.send_keys(email)
    current_address_input.send_keys(current_address)
    permanent_address_input.send_keys(permanent_address)
    time.sleep(2)
    permanent_address_input.clear()
    time.sleep(3)
    permanent_address = "Avenida Conselheiro Aguiar, s/n"
    permanent_address_input.send_keys(permanent_address)

    # Click on submit button
    # driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
    submit_button.click()

    time.sleep(5)
    
    # Map output elements
    output_name = driver.find_element(By.ID, "name")
    output_email = driver.find_element(By.ID, "email")
    output_current_address = driver.find_element(By.CSS_SELECTOR, "p#currentAddress")
    output_permanent_address = driver.find_element(By.CSS_SELECTOR, "p#permanentAddress")

    # Check output
    assert full_name in output_name.text
    assert email in output_email.text
    assert current_address in output_current_address.text
    assert permanent_address in output_permanent_address.text