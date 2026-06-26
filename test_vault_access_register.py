"""
Tests for Vault Access (Custodians) via Web UI.
"""
import pytest
from config import pages
from utilities.helpers import build_vault_access_bod_form, build_vault_access_eod_form

class TestVaultAccessBOD:
    @pytest.mark.smoke
    def test_create_access_bod_success(self, browser, teller, open_branch):
        res = browser.submit_form(pages.VAULT_ACCESS_ADD_BOD, build_vault_access_bod_form())
        assert res.is_success or "success" in res.html.lower(), \
            f"Access BOD failed. Snippet: {res.html[:500]}"

    def test_duplicate_access_bod_prevented(self, browser, teller, open_branch):
        browser.submit_form(pages.VAULT_ACCESS_ADD_BOD, build_vault_access_bod_form())
        res = browser.submit_form(pages.VAULT_ACCESS_ADD_BOD, build_vault_access_bod_form())
        is_rejected = (res.status_code == 422 or 
                       "duplicate" in res.html.lower() or 
                       "already exists" in res.html.lower())
        assert is_rejected, f"Duplicate Access BOD was NOT prevented!"

class TestVaultAccessEOD:
    def test_create_access_eod_success(self, browser, teller, open_branch):
        # Pre-req
        browser.submit_form(pages.VAULT_ACCESS_ADD_BOD, build_vault_access_bod_form())
        
        res = browser.submit_form(pages.VAULT_ACCESS_ADD_EOD, build_vault_access_eod_form())
        assert res.is_success or "success" in res.html.lower(), \
            f"Access EOD failed. Snippet: {res.html[:500]}"
