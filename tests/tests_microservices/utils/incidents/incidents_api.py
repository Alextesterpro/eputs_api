"""
HTTP client for Incidents endpoints (react API).

Endpoints covered:
- POST   /incident          - Create incident
- GET    /incident/{id}     - Get incident by ID
- PUT    /incident/{id}     - Update incident
- DELETE /incident/{id}     - Delete incident
- POST   /incident/list     - List incidents
- POST   /incident/search   - Search incidents
"""

from typing import Any, Dict, Optional
import requests

from config.auth import auth_manager, AuthConfig


class IncidentsAPI:
    """HTTP client for Incidents endpoints (react API)."""

    BASE_URL: str = AuthConfig.API_BASE_URL

    @staticmethod
    def _build_headers(extra: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """Build headers using the centralized auth manager."""
        return auth_manager.get_headers(extra)

    @classmethod
    def create_incident(
        cls,
        data: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 60,
    ) -> requests.Response:
        """POST /incident - Create a new incident."""
        req_headers = cls._build_headers(headers)
        url = f"{cls.BASE_URL}/incident"
        return requests.post(url, json=data, headers=req_headers, timeout=timeout, verify=False)

    @classmethod
    def get_incident(
        cls,
        incident_id: int,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 30,
    ) -> requests.Response:
        """GET /incident/{id} - Get incident by ID."""
        req_headers = cls._build_headers(headers)
        url = f"{cls.BASE_URL}/incident/{incident_id}"
        return requests.get(url, headers=req_headers, timeout=timeout, verify=False)

    @classmethod
    def update_incident(
        cls,
        incident_id: int,
        data: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 60,
    ) -> requests.Response:
        """PUT /incident/{id} - Update incident."""
        req_headers = cls._build_headers(headers)
        url = f"{cls.BASE_URL}/incident/{incident_id}"
        return requests.put(url, json=data, headers=req_headers, timeout=timeout, verify=False)

    @classmethod
    def delete_incident(
        cls,
        incident_id: int,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 30,
    ) -> requests.Response:
        """DELETE /incident/{id} - Delete incident."""
        req_headers = cls._build_headers(headers)
        url = f"{cls.BASE_URL}/incident/{incident_id}"
        return requests.delete(url, headers=req_headers, timeout=timeout, verify=False)

    @classmethod
    def list_incidents(
        cls,
        payload: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 60,
    ) -> requests.Response:
        """POST /incident/list - List incidents with pagination."""
        req_headers = cls._build_headers(headers)
        url = f"{cls.BASE_URL}/incident/list"
        return requests.post(url, json=payload, headers=req_headers, timeout=timeout, verify=False)

    @classmethod
    def search_incidents(
        cls,
        payload: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 60,
    ) -> requests.Response:
        """POST /incident/search - Search incidents with filters."""
        req_headers = cls._build_headers(headers)
        url = f"{cls.BASE_URL}/incident/search"
        return requests.post(url, json=payload, headers=req_headers, timeout=timeout, verify=False)


