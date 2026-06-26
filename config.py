"""
Configuration for staging Web UI URLs and test data.
"""
import os
from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class StagingConfig:
    BASE_URL: str = os.getenv("STAGING_BASE_URL", "http://127.0.0.1:8000/")
    REQUEST_TIMEOUT: int = 30
    RETRY_COUNT: int = 3
     
@dataclass
class Pages:
    LOGIN = "/accounts/login/"
    LOGOUT = "/accounts/logout/"
    DASHBOARD = "/accounts/dashboard/"
    
    BRANCH_LIST: str = "/branches"
    BRANCH_OPEN: str = "/branches/open"
    BRANCH_CLOSE: str = "/branches/close"
    
    VAULT_CASH: str = "/vault-cash"
    VAULT_CASH_ADD_BOD: str = "/vault-cash/add-bod"
    VAULT_CASH_ADD_EOD: str = "/vault-cash/add-eod"
    VAULT_CASH_ADD_IW: str = "/vault-cash/add-iw"
    VAULT_CASH_ADD_ID: str = "/vault-cash/add-id"
    
    VAULT_ACCESS: str = "/vault-access"
    VAULT_ACCESS_ADD_BOD: str = "/vault-access/add-bod"
    VAULT_ACCESS_ADD_EOD: str = "/vault-access/add-eod"

@dataclass
class TestUsers:
    MANAGER: Dict[str, str] = field(default_factory=lambda: {
        "username": os.getenv("MANAGER_USERNAME", "mgr_bkc"),
        "password": os.getenv("MANAGER_PASSWORD", "Manager@123")
    })
    ADMIN: Dict[str, str] = field(default_factory=lambda: {
        "username": os.getenv("ADMIN_USERNAME", "admin"),
        "password": os.getenv("ADMIN_PASSWORD", "Admin@123")
    })
    TELLER: Dict[str, str] = field(default_factory=lambda: {
        "username": os.getenv("TELLER_USERNAME", "teller01"),
        "password": os.getenv("TELLER_PASSWORD", "Teller@123")
    })
    STAFF: Dict[str, str] = field(default_factory=lambda: {
        "username": os.getenv("STAFF_USERNAME", "staff01"),
        "password": os.getenv("STAFF_PASSWORD", "Staff@123")
    })

@dataclass
class TestData:
    BRANCH_ID: str = os.getenv("TEST_BRANCH_ID", "BRANCH-001")
    OPENING_CASH: float = 500000.00
    CLOSING_CASH: float = 450000.00
    
    BOD_DENOMS: List[Dict] = field(default_factory=lambda: [
        {"denomination": 5000, "count": 50}, {"denomination": 1000, "count": 100},
    ])
    EOD_DENOMS: List[Dict] = field(default_factory=lambda: [
        {"denomination": 5000, "count": 45}, {"denomination": 1000, "count": 90},
    ])
    IW_DENOMS: List[Dict] = field(default_factory=lambda: [
        {"denomination": 1000, "count": 50},
    ])
    ID_DENOMS: List[Dict] = field(default_factory=lambda: [
        {"denomination": 500, "count": 60},
    ])
    BOD_CUSTODIANS: List[Dict] = field(default_factory=lambda: [
        {"employee_id": "EMP-001", "name": "John Doe"}, {"employee_id": "EMP-002", "name": "Jane Smith"},
    ])

cfg = StagingConfig()
pages = Pages()
users = TestUsers()
td = TestData()
