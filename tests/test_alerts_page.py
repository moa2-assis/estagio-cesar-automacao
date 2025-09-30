from pages.alerts_page import AlertsPage

def test_go_to_alerts_page(driver):  
    check_box_page = AlertsPage(driver)
    
    # 1
    check_box_page.navigate()

    # 2
    check_box_page.open_alerts_page_from_home()

    # 3
    check_box_page.open_alerts_page()

    # 4 + 5 + 6
    assert check_box_page.click_to_see_alert() == "You clicked a button"

    # 7 + 8 + 9
    assert check_box_page.click_to_see_alert_after_5_seconds() == "This alert appeared after 5 seconds"

    # 10 + 11 + 12 + 13
    assert check_box_page.button_confirm(accept=True) == "You selected Ok"

    # 14 + 15 + 16 + 17
    assert check_box_page.button_confirm(accept=False) == "You selected Cancel"

    # 18 + 19 + 20 + 21 + 22 + 23
    assert check_box_page.button_prompt_message("Mateuzo") == "You entered Mateuzo"