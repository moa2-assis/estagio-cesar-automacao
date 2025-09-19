from selenium.webdriver.common.by import By
import time

def test_fill_text_box_form_and_validate(driver):
    driver.get("https://demoqa.com/text-box")

    submit_button = driver.find_element(By.ID, "submit")

    # Fill out the form
    full_name_input = driver.find_element(By.ID, "userName")
    full_name = "Mateus"
    full_name_input.send_keys(full_name)

    time.sleep(1)

    email_input = driver.find_element(By.ID, "userEmail")
    email = "matt@gmail.com"
    email_input.send_keys(email)

    time.sleep(1)

    current_address_input = driver.find_element(By.ID, "currentAddress")
    current_address = "Rua Josefina, 12"
    current_address_input.send_keys(current_address)

    time.sleep(1)

    permanent_address_input = driver.find_element(By.ID, "permanentAddress")
    permanent_address = "Rua Paulina, 2321"
    permanent_address_input.send_keys(permanent_address)

    time.sleep(1)

    driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
    submit_button.click()

    time.sleep(5)

    output_name = driver.find_element(By.ID, "name")
    output_email = driver.find_element(By.ID, "email")
    output_current_address = driver.find_element(By.CSS_SELECTOR, "p#currentAddress")
    output_permanent_address = driver.find_element(By.CSS_SELECTOR, "p#permanentAddress")

    assert full_name in output_name.text
    assert email in output_email.text
    assert current_address in output_current_address.text
    assert permanent_address in output_permanent_address.text