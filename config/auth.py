"""
Authentication configuration and token management.
Best practices for API testing.
"""

import os
from typing import Optional
from datetime import datetime, timedelta
import requests


class AuthConfig:
    """Configuration for authentication and API endpoints."""
    
    # API endpoints
    API_BASE_URL = "http://91.227.17.139/services/react/api"
    AUTH_URL = "http://91.227.17.139/services/passport/api/login"  # правильный endpoint
    
    # Default token (fallback for development)
    DEFAULT_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzIiwianRpIjoiYTY1MTIzMmNkZDlkY2NjYzVmMDc2MThjOWU5ODNjYzY2MjM2M2RlNWIyZGFmM2U3MGNhZmYyZGRjMzY1MmEzNzUwMTk2OTFlZTUxZTA5OTkiLCJpYXQiOjE3NTQ2NTgxMjcuNTcyOTk5LCJuYmYiOjE3NTQ2NTgxMjcuNTczMDEsImV4cCI6MTc1NTk1NDEyNy4xMTk5MDksInN1YiI6IjY4Iiwic2NvcGVzIjpbXSwib3JnYW5pemF0aW9uX2lkX2xpc3QiOltdLCJpZGVudGlmaWVyIjoiYS52ZXNlbG92MV9BQUFfZm9ybWF0dHdvLnJ1XzE3NDg1NDYyNTYuODgzNyIsImVtYWlsIjoiYS52ZXNlbG92MUBmb3JtYXR0d28ucnUiLCJ1c2VyX25hbWUiOiJhLnZlc2Vsb3YxQGZvcm1hdHR3by5ydSIsImZpcnN0X25hbWUiOiLQkNC70LXQutGB0LDQvdC00YAiLCJsYXN0X25hbWUiOiLQktC10YHQtdC70L7QsiIsIm1pZGRsZV9uYW1lIjoi0JLQuNC60YLQvtGA0L7QstC40YcifQ.lcXCGBnkdkz9UOj1WpRnlwLOa1tCLPOcLrxTH-rKqtoIjGAuPHB6YyRjcR_J5V8tJpxBafJPcblar163S122oM0t7mq-iQLD4hHguB14lOkkWJjPjOZOL-aPlABG4M5OaJqh2dBMyp6OsJsG-yQVabxDkp7-UpHQfQ2WI3wH-WKNsHfwKFER3_KUSO3zaMm10BgWh4tFkXB9sSjJgXDmsdsbYYUGlbgpjTs43z5K_FqyvFrhpoTU5Brysb-KlsD_aJtJFUAb2ZAmuhZz0Egk5JRsEQ8jXrKhAyAf0WxNkmiOl4ojYDwrnIr691ugcRyR3foQktmqutvsq68iiINLiHEbjHHmwWHRO5c_EGcrQenjyjMJZ4IzbUnyqZDiDDCVKtm_fCpnZ-uVYWWy9aVXY2pENXyuew1LiOY86GTyF1i4KDthJT9Y0leluWJC_L2SkSVDNWbP-3Qe96xA3UbaZF-QVBmzRGIjPGEe1bjnBF2tRGrQNgMZos75q0FfGHwiy1PxylXR2-BOD4mWsKsFUnCxsDaM8KOOS5ojp7D1f5oklFsV7vSdzGCaMeEU9jQeTpvgmcNgPJmlO7Zw55wph5VQXd0l29buUIIIcJ4fJESxIunouZr6hiZqVEfsyErAXRvT6ZEU_mrfFJfXQrDZQqQmlsJxCIdLW0-e4NoF-3M"
    
    # Project settings
    PROJECT = "98_spb"
    SERVICE = "eputs"


class TokenManager:
    """Manages API tokens with automatic refresh capabilities."""
    
    def __init__(self):
        self._token: Optional[str] = None
        self._expires_at: Optional[datetime] = None
        self._refresh_threshold = timedelta(minutes=5)  # обновляем за 5 минут до истечения
    
    def get_token(self) -> str:
        """Get a valid token, refreshing if necessary."""
        if self._is_token_expired():
            self._refresh_token()
        return self._token or AuthConfig.DEFAULT_TOKEN
    
    def _is_token_expired(self) -> bool:
        """Check if token is expired or close to expiration."""
        if not self._expires_at:
            return True
        return datetime.now() + self._refresh_threshold >= self._expires_at
    
    def _refresh_token(self):
        """Refresh token from environment or use default."""
        # Priority 1: Environment variable
        env_token = os.getenv("EPUTS_TOKEN")
        if env_token:
            self._token = env_token
            # Assume environment tokens are fresh
            self._expires_at = datetime.now() + timedelta(hours=24)
            return
        
        # Priority 2: Try to load from .env file
        try:
            if os.path.exists(".env"):
                with open(".env", "r") as f:
                    for line in f:
                        if line.startswith("EPUTS_TOKEN="):
                            token = line.split("=", 1)[1].strip()
                            if token:
                                self._token = token
                                self._expires_at = datetime.now() + timedelta(hours=24)
                                return
        except Exception:
            pass
        
        # Priority 3: Use default token
        self._token = AuthConfig.DEFAULT_TOKEN
        # Default token might be expired, but we'll use it for now
        self._expires_at = datetime.now() + timedelta(hours=1)
    
    def set_token(self, token: str, expires_in_hours: int = 24):
        """Manually set a token with expiration."""
        self._token = token
        self._expires_at = datetime.now() + timedelta(hours=expires_in_hours)
    
    def clear_token(self):
        """Clear stored token."""
        self._token = None
        self._expires_at = None


class AuthManager:
    """High-level authentication manager."""
    
    def __init__(self):
        self.token_manager = TokenManager()
    
    def get_headers(self, extra: Optional[dict] = None) -> dict:
        """Build standard headers with authentication."""
        token = self.token_manager.get_token()
        
        # Handle Bearer prefix
        auth_header = f"Bearer {token}" if not token.startswith("Bearer ") else token
        
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Authorization": auth_header,
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Origin": "http://91.227.17.139",
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/140.0.0.0 Safari/537.36"
            ),
            "project": AuthConfig.PROJECT,
            "service": AuthConfig.SERVICE,
        }
        
        if extra:
            headers.update(extra)
        
        return headers
    
    def login(self, username: str, password: str) -> bool:
        """
        Attempt to login and get a new token.
        Uses the correct passport API endpoint.
        """
        try:
            payload = {
                "username": username,
                "password": password
            }
            
            headers = {
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "application/json",
                "Origin": "http://91.227.17.139",
                "Pragma": "no-cache",
                "Referer": "http://91.227.17.139/signin",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
                "service": "eputs"
            }
            
            response = requests.post(
                AuthConfig.AUTH_URL,
                json=payload,
                headers=headers,
                timeout=30,
                verify=False
            )
            
            if response.status_code == 200:
                data = response.json()
                if "token" in data:
                    self.token_manager.set_token(data["token"])
                    return True
                elif "access_token" in data:
                    self.token_manager.set_token(data["access_token"])
                    return True
                else:
                    print(f"Unexpected response format: {data}")
                    return False
            
            return False
            
        except Exception as e:
            print(f"Login failed: {e}")
            return False


# Global instance
auth_manager = AuthManager()
