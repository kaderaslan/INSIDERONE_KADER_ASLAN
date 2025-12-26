from pages.careers_qa_page import CareersQAPage
from pages.open_positions_page import OpenPositionsPage


def test_filter_qa_jobs(driver):
    qa_page = CareersQAPage(driver)
    open_positions = OpenPositionsPage(driver)

    qa_page.open_qa_page()

    assert qa_page.is_qa_page_opened()
    assert qa_page.is_header_visible()
    assert qa_page.is_footer_visible()

    qa_page.click_see_all_qa_jobs()

    open_positions.filter_by_department("Quality Assurance")
    open_positions.filter_by_location("Istanbul")
    open_positions.assert_all_jobs_in_location("istanbul")
    job_cards = open_positions.get_all_job_cards()
    assert len(job_cards) > 0

    istanbul_jobs = []

    for i in range(len(job_cards)):
        details = open_positions.get_job_details_by_index(i)
        if "istanbul" in details["location"].lower():
            istanbul_jobs.append(details)

    assert len(istanbul_jobs) > 0, "No Istanbul jobs found after filtering"


def test_view_role_redirects_to_lever_application(driver):
    qa_page = CareersQAPage(driver)
    open_positions = OpenPositionsPage(driver)

    qa_page.open_qa_page()
    qa_page.click_see_all_qa_jobs()

    open_positions.filter_by_department("Quality Assurance")
    open_positions.filter_by_location("Istanbul")

    job_cards = open_positions.get_all_job_cards()
    assert len(job_cards) > 0

    open_positions.click_view_role_by_index(0)
    open_positions.switch_to_lever_page()

    assert "lever.co" in driver.current_url.lower()