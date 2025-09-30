from pages.slider_page import SliderPage

value_test = 91

def test_go_to_alerts_page(driver):  
    slider_page = SliderPage(driver)
    
    # 1
    slider_page.navigate()

    # 2
    slider_page.open_widgets_page_from_home()

    # 3
    slider_page.open_slider_page()

    # 5
    slider_page.set_slider_value_while(value_test)

    assert slider_page.get_slider_value() == value_test