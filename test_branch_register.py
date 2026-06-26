"""
Tests for Branch Open/Close via Web UI.
"""
import pytest  # type: ignore[import]
from config import cfg, pages
from utilities.helpers import build_open_form, build_close_form

class TestBranchOpen:
    @pytest.mark.smoke
    def test_manager_can_open_branch(self, browser, manager, closed_branch):
        res = browser.submit_form(pages.BRANCH_OPEN, build_open_form())
        assert res.is_success or "open" in res.html.lower() or res.status_code == 302, \
            f"Failed to open branch. Status: {res.status_code}, Snippet: {res.html[:500]}"
        # Verify state changed (Look for "OPEN" text in the response or redirected page)
        verify = browser.get_page(pages.BRANCH_LIST)
        assert verify.contains_text("OPEN") or verify.contains_text("open"), \
            "Branch status page does not show OPEN after opening."

    def test_teller_cannot_open_branch(self, browser, teller, closed_branch):
        res = browser.submit_form(pages.BRANCH_OPEN, build_open_form())
        # Expect forbidden (403), redirect to login, or permission denied text
        is_blocked = (res.status_code == 403 or 
                      "forbidden" in res.html.lower() or 
                      "permission" in res.html.lower() or
                      "login" in res.url)
        assert is_blocked, f"Teller was able to open branch! Status: {res.status_code}"

class TestBranchClose:
    @pytest.mark.smoke
    def test_manager_can_close_branch(self, browser, manager, open_branch):
        res = browser.submit_form(pages.BRANCH_CLOSE, build_close_form())
        assert res.is_success or "close" in res.html.lower() or res.status_code == 302, \
            f"Failed to close branch. Status: {res.status_code}"
        
        verify = browser.get_page(pages.BRANCH_LIST)
        assert verify.contains_text("CLOSED") or verify.contains_text("closed"), \
            "Branch status page does not show CLOSED after closing."

    def test_teller_cannot_close_branch(self, browser, teller, open_branch):
        res = browser.submit_form(pages.BRANCH_CLOSE, build_close_form())
        is_blocked = (res.status_code == 403 or 
                      "forbidden" in res.html.lower() or 
                      "permission" in res.html.lower() or
                      "login" in res.url)
        assert is_blocked, f"Teller was able to close branch! Status: {res.status_code}"
