"""
Tests for Vault Cash (BOD, EOD, IW, ID) via Web UI.
"""
import pytest
from config import pages
from utilities.helpers import (
    build_vault_cash_bod_form, build_vault_cash_eod_form,
    build_vault_cash_iw_form, build_vault_cash_id_form
)

class TestVaultCashBOD:
    @pytest.mark.smoke
    def test_create_bod_success(self, browser, teller, open_branch):
        res = browser.submit_form(pages.VAULT_CASH_ADD_BOD, build_vault_cash_bod_form())
        assert res.is_success or "success" in res.html.lower() or "saved" in res.html.lower(), \
            f"BOD Creation failed. Status: {res.status_code}, Snippet: {res.html[:500]}"

    def test_duplicate_bod_prevented(self, browser, teller, open_branch):
        # First attempt
        browser.submit_form(pages.VAULT_CASH_ADD_BOD, build_vault_cash_bod_form())
        # Second attempt
        res = browser.submit_form(pages.VAULT_CASH_ADD_BOD, build_vault_cash_bod_form())
        is_rejected = (res.status_code == 422 or 
                       "duplicate" in res.html.lower() or 
                       "already exists" in res.html.lower() or
                       "already been" in res.html.lower())
        assert is_rejected, f"Duplicate BOD was NOT prevented! Snippet: {res.html[:500]}"

    def test_bod_blocked_when_branch_closed(self, browser, teller, closed_branch):
        res = browser.submit_form(pages.VAULT_CASH_ADD_BOD, build_vault_cash_bod_form())
        is_blocked = (res.status_code in [400, 403, 422] or 
                      "must be open" in res.html.lower() or 
                      "branch is closed" in res.html.lower())
        assert is_blocked, f"BOD allowed on closed branch! Snippet: {res.html[:500]}"

class TestVaultCashEOD:
    def test_create_eod_success(self, browser, teller, open_branch):
        # Pre-requisite: BOD
        browser.submit_form(pages.VAULT_CASH_ADD_BOD, build_vault_cash_bod_form())
        
        res = browser.submit_form(pages.VAULT_CASH_ADD_EOD, build_vault_cash_eod_form())
        assert res.is_success or "success" in res.html.lower(), \
            f"EOD Creation failed. Snippet: {res.html[:500]}"

class TestIntermediateEntries:
    def test_multiple_iw_allowed(self, browser, teller, open_branch):
        for i in range(3):
            res = browser.submit_form(pages.VAULT_CASH_ADD_IW, build_vault_cash_iw_form())
            assert res.is_success or "success" in res.html.lower(), \
                f"IW #{i+1} failed. Snippet: {res.html[:500]}"

    def test_multiple_id_allowed(self, browser, teller, open_branch):
        for i in range(3):
            res = browser.submit_form(pages.VAULT_CASH_ADD_ID, build_vault_cash_id_form())
            assert res.is_success or "success" in res.html.lower(), \
                f"ID #{i+1} failed. Snippet: {res.html[:500]}"
