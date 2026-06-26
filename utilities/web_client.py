"""
Web Client wrapper to simulate browser behavior using requests + BeautifulSoup.
Handles cookies, CSRF tokens, and form parsing automatically.
"""
from os import path
import time
import logging
from typing import Dict, Optional, Tuple
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

from config import cfg, pages

logger = logging.getLogger(__name__)

@dataclass
class WebResponse:
    status_code: int
    url: str
    html: str
    soup: Optional[BeautifulSoup] = None
    is_success: bool = False
    error: Optional[str] = None

    def contains_text(self, text: str) -> bool:
        return text.lower() in self.html.lower()

    def get_form_action(self, form_id: Optional[str] = None) -> Optional[str]:
        if not self.soup: return None
        form = self.soup.find("form", id=form_id) if form_id else self.soup.find("form")
        return form.get("action") if form else None

class WebClient:
    def __init__(self):
        self.base_url = cfg.BASE_URL
        self.session = requests.Session()
        # Mimic a standard browser
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def _build_url(self, path: str) -> str:
        if path.startswith(("http://", "https://")):
            return path
        return f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"

    def get_page(self, path: str, **kwargs) -> WebResponse:
        url = self._build_url(path)
        try:
            resp = self.session.get(url, timeout=cfg.REQUEST_TIMEOUT, verify=False, **kwargs)
            soup = BeautifulSoup(resp.text, 'html.parser')
            return WebResponse(
                status_code=resp.status_code, url=resp.url, html=resp.text,
                soup=soup, is_success=resp.ok
            )
        except Exception as e:
            return WebResponse(status_code=0, url=url, html="", error=str(e))

    def submit_form(self, path: str, data: Dict, method: str = "POST", **kwargs) -> WebResponse:
        url = self._build_url(path)
        
        # 1. Fetch the page to get CSRF token and hidden fields
        try:
            get_resp = self.session.get(url, timeout=cfg.REQUEST_TIMEOUT, verify=False)
            soup = BeautifulSoup(get_resp.text, 'html.parser')
        except Exception as e:
            return WebResponse(status_code=0, url=url, html="", error=f"Failed to fetch form page: {e}")

        # 2. Extract CSRF token (common patterns: _token, csrf_token, csrfmiddlewaretoken)
        csrf_input = soup.find("input", {"name": ["_token", "csrf_token", "csrfmiddlewaretoken", "authenticity_token"]})
        if csrf_input and csrf_input.get("value"):
            data[csrf_input.get("name")] = csrf_input.get("value")

        # 3. Extract all other hidden inputs and merge them
        for hidden in soup.find_all("input", {"type": "hidden"}):
            name = hidden.get("name")
            if name and name not in data:
                data[name] = hidden.get("value", "")

        # 4. Submit the form
        try:
            if method.upper() == "POST":
                post_resp = self.session.post(url, data=data, timeout=cfg.REQUEST_TIMEOUT, verify=False, **kwargs)
            else:
                post_resp = self.session.put(url, data=data, timeout=cfg.REQUEST_TIMEOUT, verify=False, **kwargs)
            
            post_soup = BeautifulSoup(post_resp.text, 'html.parser')
            return WebResponse(
                status_code=post_resp.status_code, url=post_resp.url, html=post_resp.text,
                soup=post_soup, is_success=post_resp.ok
            )
        except Exception as e:
            return WebResponse(status_code=0, url=url, html="", error=f"Form submission failed: {e}")

    def logout(self):
        self.session.get(self._build_url(pages.LOGOUT), verify=False)
        self.session.cookies.clear()

    def close(self):
        self.session.close()
