from pages.careers_page import CareersPage


def test_careers_page_loaded(driver):
    careers_page = CareersPage(driver)

    careers_page.open_careers_page()

    assert careers_page.is_careers_page_opened()
    assert careers_page.is_header_visible()
    assert careers_page.is_footer_visible()
