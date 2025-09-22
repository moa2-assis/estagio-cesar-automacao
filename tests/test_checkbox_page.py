from pages.check_box_page import CheckBoxPage
import time

# def test_expand_all(driver):
#     check_box_page = CheckBoxPage(driver)
#     check_box_page.navigate()

#     check_box_page.expand_all_click()
#     time.sleep(1)

def test_commands_checkbox_output(driver):  
    check_box_page = CheckBoxPage(driver)
    check_box_page.navigate()

    check_box_page.expand_all_click()
    check_box_page.commands_checkbox_click()
    time.sleep(1)
    # check_box_page.check_commands_input()

    time.sleep(1)
    assert check_box_page.commands_checkbox_output()
    time.sleep(1)

# def test_notes_checkbox_output(driver):
#     check_box_page = CheckBoxPage(driver)
#     check_box_page.navigate()

#     check_box_page.expand_all_click()
#     time.sleep(1)

#     check_box_page.notes_checkbox_click()
#     time.sleep(1)
#     check_box_page.notes_checkbox_output()
#     assert check_box_page.notes_input.is_selected()