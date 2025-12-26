from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CareersPage(BasePage):

    CAREERS_URL = "https://insiderone.com/careers"

    HEADER = (By.ID, "navigation")
    FOOTER = (By.ID, "footer")
    LOGO = (By.CSS_SELECTOR, ".header-logo a")

    def open_careers_page(self):
        self.driver.get(self.CAREERS_URL)
        self.reject_cookies_if_present()

    def is_careers_page_opened(self):
        return self.CAREERS_URL in self.driver.current_url

    def is_header_visible(self):
        return self.is_element_visible(self.HEADER)

    def is_footer_visible(self):
        return self.is_element_visible(self.FOOTER)

    def is_logo_visible(self):
        return self.is_element_visible(self.LOGO)
