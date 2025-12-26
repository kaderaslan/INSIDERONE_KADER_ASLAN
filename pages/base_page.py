from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import time


class BasePage:
    def __init__(self, driver, timeout=15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # -----------------------------
    # Navigation
    # -----------------------------
    def open(self, url: str):
        self.driver.get(url)

    def get_current_url(self) -> str:
        return self.driver.current_url

    # -----------------------------
    # Wait helpers
    # -----------------------------
    def wait_for_presence(self, locator: tuple):
        return self.wait.until(EC.presence_of_element_located(locator))

    def wait_for_visibility(self, locator: tuple):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_for_clickable(self, locator: tuple):
        return self.wait.until(EC.element_to_be_clickable(locator))

    # -----------------------------
    # Element helpers
    # -----------------------------
    def safe_click(self, locator: tuple, post_condition=None):
        """
        Click element safely and optionally wait for post condition
        """
        element = self.wait_for_clickable(locator)

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            element
        )

        time.sleep(0.2)
        element.click()

        if post_condition:
            self.wait.until(post_condition)

    def type(self, locator: tuple, text: str, clear: bool = True):
        element = self.wait_for_visibility(locator)
        if clear:
            element.clear()
        element.send_keys(text)

    def get_text(self, locator: tuple) -> str:
        return self.wait_for_visibility(locator).text

    def get_elements(self, locator: tuple):
        self.wait_for_presence(locator)
        return self.driver.find_elements(*locator)

    def is_element_visible(self, locator: tuple) -> bool:
        try:
            self.wait_for_visibility(locator)
            return True
        except TimeoutException:
            return False

    # -----------------------------
    # Dropdown helper
    # -----------------------------
    def select_dropdown_by_partial_text(self, locator: tuple, partial_text: str):
        """
        Select dropdown option containing partial text
        """
        select = Select(self.wait_for_clickable(locator))

        self.wait.until(lambda d: len(select.options) > 1)

        for option in select.options:
            if partial_text.lower() in option.text.lower():
                option.click()
                return

        raise Exception(f"Option containing '{partial_text}' not found")

    # -----------------------------
    # Window / redirect helpers
    # -----------------------------
    def switch_to_lever_page(self):
        """
        Switches to Lever application tab
        """
        def _lever_opened(driver):
            for handle in driver.window_handles:
                driver.switch_to.window(handle)
                if "lever.co" in driver.current_url.lower():
                    return True
            return False

        self.wait.until(_lever_opened)

        for handle in self.driver.window_handles:
            self.driver.switch_to.window(handle)
            if "lever.co" in self.driver.current_url.lower():
                return

        raise TimeoutException("Lever page not found")

    # -----------------------------
    # Cookie handling
    # -----------------------------
    COOKIE_REJECT = (By.ID, "wt-cli-reject-btn")
    COOKIE_BAR = (By.ID, "cookie-law-info-bar")

    def reject_cookies_if_present(self):
        """
        Reject cookies if cookie banner is present
        """
        try:
            reject_btn = self.wait.until(
                EC.element_to_be_clickable(self.COOKIE_REJECT)
            )
            reject_btn.click()

            self.wait.until(
                EC.invisibility_of_element_located(self.COOKIE_BAR)
            )
        except TimeoutException:
            pass
