from pages.text_box_page import TextBoxPage
import time

def test_fill_form_with_pom(driver):
    text_box_page = TextBoxPage(driver)
    text_box_page.navigate()

    # Test Data
    full_name = "Mateuzo"
    email = "mateuzo@gmail.com"
    current_address = "Rua Bolinha"
    permanent_address = "Rua Quadradinho"

    # Fill and submit
    text_box_page.fill_form(full_name, email, current_address, permanent_address)
    time.sleep(2)
    text_box_page.submit()

    output_ = text_box_page.get_output_text()
    
    assert full_name in output_
    assert email in output_
    assert current_address in output_
    assert permanent_address in output_