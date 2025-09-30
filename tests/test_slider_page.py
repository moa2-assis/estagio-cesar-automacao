from pages.alerts_page import SliderPage

def test_go_to_alerts_page(driver):  
    slider_page = SliderPage(driver)
    
    # 1
    slider_page.navigate()

    # 2
    slider_page.open_widgets_page_from_home()

    # 3
    slider_page.open_slider_page()

    # 4 + 5
    assert slider_page.set_slider_value(73) == 73