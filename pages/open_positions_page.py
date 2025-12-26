from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import StaleElementReferenceException
from pages.base_page import BasePage


class OpenPositionsPage(BasePage):

    # ---------------- LOCATORS ----------------
    LOCATION_FILTER = (By.ID, "filter-by-location")
    DEPARTMENT_FILTER = (By.ID, "filter-by-department")
    JOBS_CONTAINER = (By.ID, "jobs-list")
    JOB_CARDS = (By.CSS_SELECTOR, "#jobs-list .position-list-item")

    JOB_TITLE = (By.CSS_SELECTOR, ".position-title")
    JOB_DEPARTMENT = (By.CSS_SELECTOR, ".position-department")
    JOB_LOCATION = (By.CSS_SELECTOR, ".position-location")

    VIEW_ROLE_BUTTON = (By.LINK_TEXT, "View Role")

    # ---------------- WAITS ----------------
    def wait_until_jobs_stable(self):
        """
        Wait until job cards are rendered and texts are non-empty
        (SPA-safe, React-safe)
        """

        def _jobs_ready(driver):
            try:
                cards = driver.find_elements(*self.JOB_CARDS)
                if not cards:
                    return False

                for card in cards:
                    if (
                            card.find_element(*self.JOB_TITLE).text.strip() == "" or
                            card.find_element(*self.JOB_DEPARTMENT).text.strip() == "" or
                            card.find_element(*self.JOB_LOCATION).text.strip() == ""
                    ):
                        return False
                return True
            except StaleElementReferenceException:
                return False

        self.wait.until(_jobs_ready)

    def wait_until_jobs_rendered(self):
        self.wait.until(EC.presence_of_all_elements_located(self.JOB_CARDS))
        self.wait.until(lambda d: len(d.find_elements(*self.JOB_CARDS)) > 0)

    # ---------------- ACTIONS ----------------
    def filter_by_department(self, department_text: str):
        select = Select(self.wait.until(
            EC.element_to_be_clickable(self.DEPARTMENT_FILTER)
        ))

        self.wait.until(lambda d: len(select.options) > 1)

        select.select_by_visible_text(department_text)
        self.wait_until_jobs_rendered()

    def filter_by_location(self, location_text: str):
        select = Select(self.wait.until(
            EC.element_to_be_clickable(self.LOCATION_FILTER)
        ))

        self.wait.until(lambda d: len(select.options) > 1)

        select.select_by_visible_text(location_text)
        self.wait_until_jobs_rendered()

        # 🔥 WAIT UNTIL FILTER APPLIED
        def _location_applied(driver):
            try:
                cards = driver.find_elements(*self.JOB_CARDS)
                if not cards:
                    return False

                for card in cards:
                    loc = card.get_attribute("data-location")
                    if location_text.lower() not in loc.lower():
                        return False
                return True
            except StaleElementReferenceException:
                return False

        self.wait.until(_location_applied)

    def assert_all_jobs_in_location(self, expected: str):
        self.wait.until(
            lambda d: all(
                expected.lower() in card.get_attribute("data-location").lower()
                for card in d.find_elements(*self.JOB_CARDS)
            )
        )

    def get_all_job_cards(self):
        return self.driver.find_elements(*self.JOB_CARDS)

    def get_all_job_details(self):
        return [{"title": card.find_element(*self.JOB_TITLE).text.strip(),
                 "department": card.find_element(*self.JOB_DEPARTMENT).text.strip(),
                 "location": card.find_element(*self.JOB_LOCATION).text.strip()} for card in
                self.driver.find_elements(*self.JOB_CARDS)]

    def get_job_details_by_index(self, index: int):
        cards = self.get_all_job_cards()
        card = cards[index]

        return {
            "title": card.find_element(*self.JOB_TITLE).text.strip(),
            "department": card.find_element(*self.JOB_DEPARTMENT).text.strip(),
            "location": card.find_element(*self.JOB_LOCATION).text.strip()
        }

    def click_view_role_by_index(self, index: int):
        self.wait_until_jobs_stable()

        cards = self.driver.find_elements(*self.JOB_CARDS)
        card = cards[index]

        button = card.find_element(*self.VIEW_ROLE_BUTTON)

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", button
        )

        self.wait.until(EC.element_to_be_clickable(button))
        button.click()