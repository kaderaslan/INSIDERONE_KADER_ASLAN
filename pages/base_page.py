from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import time


class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url: str):
        self.driver.get(url)


    def get_current_url(self) -> str:
        return self.driver.current_url

    def wait_for_elements(self, locator: tuple):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def wait_for_presence(self, locator: tuple):
        return self.wait.until(EC.presence_of_element_located(locator))

    def wait_for_clickable(self, locator: tuple):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def safe_click(self, locator, post_condition=None):
        element = self.wait.until(EC.element_to_be_clickable(locator))

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            element
        )

        time.sleep(0.2)
        element.click()

        if post_condition:
            self.wait.until(post_condition)

    def wait_for_visibility(self, locator):
        return self.wait.until(
            EC.visibility_of_element_located(locator)
        )

    def type(self, locator: tuple, text: str, clear: bool = True):
        element = self.wait_for_visibility(locator)
        if clear:
            element.clear()
        element.send_keys(text)

    def get_text(self, locator: tuple) -> str:
        element = self.wait_for_visibility(locator)
        return element.text

    def is_element_visible(self, locator: tuple) -> bool:
        try:
            self.wait_for_visibility(locator)
            return True
        except TimeoutException:
            return False

    def get_elements(self, locator: tuple):
        self.wait_for_presence(locator)
        return self.driver.find_elements(*locator)

    def select_dropdown_by_partial_text(self, locator, partial_text):
        select = Select(self.wait_for_clickable(locator))

        self.wait.until(lambda d: len(select.options) > 1)

        for option in select.options:
            if partial_text.lower() in option.text.lower():
                option.click()
                return

        raise Exception(f"Option containing '{partial_text}' not found")

    def wait_for_page_anchor(self, locator: tuple):
        self.wait.until(EC.visibility_of_element_located(locator))

    def switch_to_lever_page(self):
        def _lever_opened(driver):
            for w in driver.window_handles:
                driver.switch_to.window(w)
                if "lever.co" in driver.current_url.lower():
                    return True
            return False

        self.wait.until(_lever_opened)

        # Final switch (garanti)
        for w in self.driver.window_handles:
            self.driver.switch_to.window(w)
            if "lever.co" in self.driver.current_url.lower():
                return

        raise TimeoutException("Lever page not found")

    COOKIE_REJECT = (By.ID, "wt-cli-reject-btn")
    COOKIE_BAR = (By.ID, "cookie-law-info-bar")

    def reject_cookies_if_present(self):
        try:
            reject_btn = self.wait.until(
                EC.element_to_be_clickable(self.COOKIE_REJECT)
            )
            reject_btn.click()

            # banner DOM’dan ya da görünümden kaybolana kadar bekle
            self.wait.until(
                EC.invisibility_of_element_located(self.COOKIE_BAR)
            )
        except TimeoutException:
            pass


