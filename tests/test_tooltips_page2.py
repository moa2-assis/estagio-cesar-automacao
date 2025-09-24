from pages.tool_tips_page2 import TooltipsPage2
import time
import pytest

@pytest.mark.smoke
def test_hover_tool_tip_button(driver):  
    tool_tips_page = TooltipsPage2(driver)
    tool_tips_page.navigate()
    tool_tips_page.tool_tip_button_hover()

    assert tool_tips_page.tool_tip_button_hover_tooltip_text() == "You hovered over the Button"

@pytest.mark.smoke
def test_hover_tool_tip_text_field(driver):  
    tool_tips_page = TooltipsPage2(driver)
    tool_tips_page.navigate()
    tool_tips_page.tool_tip_text_hover()

    assert tool_tips_page.tool_tip_text_field_hover_text() == "You hovered over the text field"