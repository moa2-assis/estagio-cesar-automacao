from pages.tool_tips_page import TooltipsPage
import pytest
from utils.data_loader import load_json_data

test_data = load_json_data("data/test_data.json")

@pytest.mark.smoke
def test_hover_tool_tip_button(driver):  
    tool_tips_page = TooltipsPage(driver)
    tool_tips_page.navigate(test_data["tool_tips_url"])
    tool_tips_page.tooltip_button_hover()

    assert tool_tips_page.tooltip_button_hover_text() == test_data["tool_tip_button_text"]

@pytest.mark.smoke
def test_hover_tool_tip_text_field(driver):  
    tool_tips_page = TooltipsPage(driver)
    tool_tips_page.navigate(test_data["tool_tips_url"])
    tool_tips_page.tooltip_text_field_hover()

    assert tool_tips_page.tooltip_text_field_hover_text() == test_data["tool_tip_field_text"]