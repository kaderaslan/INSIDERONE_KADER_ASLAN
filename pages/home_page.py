from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class HomePage(BasePage):

    URL = "https://insiderone.com/"

    HEADER = (By.ID, "navigation")
    FOOTER = (By.TAG_NAME, "footer")

    HERO_SECTION = (By.CSS_SELECTOR, "section.homepage-hero")
    CORE_DIFFERENTIATORS = (By.CSS_SELECTOR, "section.homepage-core-differentiators")
    SOCIAL_PROOF = (By.CSS_SELECTOR, "section.homepage-social-proof")

    def open_home_page(self):
        self.open(self.URL)
        self.reject_cookies_if_present()

    def is_home_page_opened(self) -> bool:
        return self.URL in self.get_current_url()

    def are_main_blocks_visible(self) -> bool:
        """
        Verifies homepage main content blocks are loaded.
        Main blocks are defined as core layout sections.
        """
        return all([
            self.is_element_visible(self.HEADER),
            self.is_element_visible(self.HERO_SECTION),
            self.is_element_visible(self.CORE_DIFFERENTIATORS),
            self.is_element_visible(self.SOCIAL_PROOF),
            self.is_element_visible(self.FOOTER)
        ])
