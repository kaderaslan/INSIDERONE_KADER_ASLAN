from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC


class CareersQAPage(BasePage):

    QA_URL = "https://insiderone.com/careers/quality-assurance/"

    HEADER = (By.ID, "navigation")
    FOOTER = (By.ID, "footer")

    SEE_ALL_QA_JOBS = (By.LINK_TEXT, "See all QA jobs")

    # Open Positions page unique element
    LOCATION_FILTER = (By.ID, "filter-by-location")
    OPEN_POSITIONS_CONTAINER = (By.ID, "jobs-list")

    def open_qa_page(self):
        self.open(self.QA_URL)
        self.reject_cookies_if_present()

    def is_qa_page_opened(self):
        return "quality-assurance" in self.get_current_url()

    def is_header_visible(self):
        return self.is_element_visible(self.HEADER)

    def is_footer_visible(self):
        return self.is_element_visible(self.FOOTER)

    def click_see_all_qa_jobs(self):
        self.safe_click(
            self.SEE_ALL_QA_JOBS,
            post_condition=EC.visibility_of_element_located(self.LOCATION_FILTER)
        )




    # def click_see_all_qa_jobs(self):
    #     self.click(self.SEE_ALL_QA_JOBS)
    #
    #     # ✅ URL yerine SAYFA identity element bekle
    #     self.wait_for_visibility(self.LOCATION_FILTER)


