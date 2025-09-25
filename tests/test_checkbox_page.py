from pages.check_box_page import CheckBoxPage
import time

def test_commands_checkbox_output(driver):  
    check_box_page = CheckBoxPage(driver)
    check_box_page.navigate()

    check_box_page.expand_all_click()
    check_box_page.commands_checkbox_click()

    time.sleep(1)
    assert check_box_page.commands_checkbox_output()

def test_notes_checkbox_output(driver):
    check_box_page = CheckBoxPage(driver)
    check_box_page.navigate()

    check_box_page.expand_all_click()
    check_box_page.notes_checkbox_click()
    
    time.sleep(1)
    assert check_box_page.notes_checkbox_output()
()