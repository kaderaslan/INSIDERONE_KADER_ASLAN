from pages.home_page import HomePage


def test_insider_home_page_loaded(driver):
    """
    Verify Insider home page is opened
    and main blocks are visible
    """
    home_page = HomePage(driver)

    home_page.open_home_page()

    assert home_page.is_home_page_opened(), "Home page URL is not correct"
    assert home_page.are_main_blocks_visible(), "One or more main blocks are not visible"
