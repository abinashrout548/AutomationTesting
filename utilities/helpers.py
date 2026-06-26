"""
Helper functions to build form payloads for UI submission.
"""
from datetime import date
from typing import Dict, List
from config import td

def today_str() -> str:
    return date.today().isoformat()

def build_open_form(override: Dict = None) -> Dict:
    data = {
        "branch_id": td.BRANCH_ID,
        "date": today_str(),
        "opening_cash_balance": td.OPENING_CASH,
        "notes": "Automated Test - Open Branch"
    }
    if override: data.update(override)
    return data

def build_close_form(override: Dict = None) -> Dict:
    data = {
        "branch_id": td.BRANCH_ID,
        "date": today_str(),
        "closing_cash_balance": td.CLOSING_CASH,
        "notes": "Automated Test - Close Branch"
    }
    if override: data.update(override)
    return data

def build_denom_form_data(denominations: List[Dict], prefix: str = "denoms") -> Dict:
    """Converts a list of denominations into flat form data (e.g., denoms[0][denomination]=5000)."""
    data = {}
    for i, d in enumerate(denominations):
        for key, val in d.items():
            data[f"{prefix}[{i}][{key}]"] = val
    return data

def build_vault_cash_bod_form() -> Dict:
    data = {"branch_id": td.BRANCH_ID, "date": today_str(), "entry_type": "BOD"}
    data.update(build_denom_form_data(td.BOD_DENOMS))
    return data

def build_vault_cash_eod_form() -> Dict:
    data = {"branch_id": td.BRANCH_ID, "date": today_str(), "entry_type": "EOD"}
    data.update(build_denom_form_data(td.EOD_DENOMS))
    return data

def build_vault_cash_iw_form() -> Dict:
    data = {"branch_id": td.BRANCH_ID, "date": today_str(), "entry_type": "IW", "purpose": "ATM Replenishment"}
    data.update(build_denom_form_data(td.IW_DENOMS))
    return data

def build_vault_cash_id_form() -> Dict:
    data = {"branch_id": td.BRANCH_ID, "date": today_str(), "entry_type": "ID", "source": "Counter Deposit"}
    data.update(build_denom_form_data(td.ID_DENOMS))
    return data

def build_vault_access_bod_form() -> Dict:
    data = {"branch_id": td.BRANCH_ID, "date": today_str(), "entry_type": "BOD", "purpose": "Morning Vault Open"}
    for i, c in enumerate(td.BOD_CUSTODIANS):
        data[f"custodians[{i}][employee_id]"] = c["employee_id"]
        data[f"custodians[{i}][name]"] = c["name"]
    return data

def build_vault_access_eod_form() -> Dict:
    data = {"branch_id": td.BRANCH_ID, "date": today_str(), "entry_type": "EOD", "purpose": "Evening Vault Close"}
    for i, c in enumerate(td.BOD_CUSTODIANS):
        data[f"custodians[{i}][employee_id]"] = c["employee_id"]
        data[f"custodians[{i}][name]"] = c["name"]
    return data
