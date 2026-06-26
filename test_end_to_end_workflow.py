"""
Full Daily Workflow E2E Test via Web UI.
"""
import pytest
from config import pages
from utilities.helpers import (
    build_open_form, build_close_form,
    build_vault_cash_bod_form, build_vault_cash_eod_form,
    build_vault_cash_iw_form, build_vault_cash_id_form,
    build_vault_access_bod_form, build_vault_access_eod_form
)

@pytest.mark.e2e
def test_complete_daily_workflow(browser, manager, teller):
    """
    1. Manager Opens Branch
    2. Teller adds BOD (Cash & Access)
    3. Teller adds IW and ID
    4. Teller adds EOD (Cash & Access)
    5. Manager Closes Branch
    """
    # 1. Morning: Manager opens branch
    res = browser.submit_form(pages.BRANCH_OPEN, build_open_form())
    assert res.is_success or "open" in res.html.lower(), "Step 1 Failed: Could not open branch"
    
    verify = browser.get_page(pages.BRANCH_LIST)
    assert verify.contains_text("OPEN"), "Step 1 Failed: Branch status not OPEN"

    # Switch to Teller
    from tests.utilities.auth import WebAuthManager
    auth = WebAuthManager(browser)
    auth.login("teller")

    # 2. Day: Teller creates BODs
    res = browser.submit_form(pages.VAULT_CASH_ADD_BOD, build_vault_cash_bod_form())
    assert res.is_success or "success" in res.html.lower(), "Step 2 Failed: Vault Cash BOD"
    
    res = browser.submit_form(pages.VAULT_ACCESS_ADD_BOD, build_vault_access_bod_form())
    assert res.is_success or "success" in res.html.lower(), "Step 2 Failed: Vault Access BOD"

    # 3. Day: Intermediate entries
    res = browser.submit_form(pages.VAULT_CASH_ADD_IW, build_vault_cash_iw_form())
    assert res.is_success or "success" in res.html.lower(), "Step 3 Failed: IW"
    
    res = browser.submit_form(pages.VAULT_CASH_ADD_ID, build_vault_cash_id_form())
    assert res.is_success or "success" in res.html.lower(), "Step 3 Failed: ID"

    # 4. Evening: Teller creates EODs
    res = browser.submit_form(pages.VAULT_CASH_ADD_EOD, build_vault_cash_eod_form())
    assert res.is_success or "success" in res.html.lower(), "Step 4 Failed: Vault Cash EOD"
    
    res = browser.submit_form(pages.VAULT_ACCESS_ADD_EOD, build_vault_access_eod_form())
    assert res.is_success or "success" in res.html.lower(), "Step 4 Failed: Vault Access EOD"

    # 5. Evening: Manager closes branch
    auth.login("manager")
    res = browser.submit_form(pages.BRANCH_CLOSE, build_close_form())
    assert res.is_success or "close" in res.html.lower(), "Step 5 Failed: Could not close branch"
    
    verify = browser.get_page(pages.BRANCH_LIST)
    assert verify.contains_text("CLOSED"), "Step 5 Failed: Branch status not CLOSED"
