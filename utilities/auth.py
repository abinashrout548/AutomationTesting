"""
Handles UI-based login/logout by submitting the login form.
"""
from config import pages, users
from utilities.web_client import WebClient, WebResponse

class WebAuthManager:
    def __init__(self, client: WebClient):
        self.client = client
        self._current_role = None

    def login(self, role: str) -> WebResponse:
        creds = getattr(users, role.upper(), None)
        if not creds:
            raise ValueError(f"No credentials for role: {role}")
        
        self.client.logout() # Clear old session
        response = self.client.submit_form(
            path=pages.LOGIN,
            data={"username": creds["username"], "password": creds["password"]}
        )
        
        # Assuming successful login redirects (3xx) or shows dashboard/success message
        if response.status_code in [200, 302] or response.is_success or "dashboard" in response.url:
            self._current_role = role
        else:
            raise AssertionError(f"Login failed for {role}. Status: {response.status_code}, HTML snippet: {response.html[:500]}")
        
        return response

    def get_current_role(self) -> str:
        return self._current_role
